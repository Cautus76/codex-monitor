"""Build and install in temporary directories, without touching the real panel."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    source = base / 'source'
    source.mkdir()
    for name in ('install.sh', 'uninstall.sh', 'Indicator.vala', 'codex-limits.py'):
        shutil.copy2(root / name, source / name)
    bindir = base / 'bin'
    bindir.mkdir()
    plugins = base / 'plugins'
    plugins.mkdir()
    home = base / 'home'
    home.mkdir()
    wrappers = {
        'sudo': '#!/bin/bash\nif [[ "$1" == -v ]]; then exit 0; fi\nexec "$@"\n',
        'pkg-config': f'#!/bin/bash\nif [[ "$1" == --variable=indicatorsdir ]]; then echo "{plugins}"; else exec /usr/bin/pkg-config "$@"; fi\n',
        'codex': '''#!/usr/bin/python3
import sys, json
if sys.argv[1:] in (['login','status'], ['app-server','--help']):
    sys.exit(0)
for line in sys.stdin:
    msg=json.loads(line)
    if 'id' in msg:
        result = {} if msg['id']==1 else {'rateLimits':{'primary':{'usedPercent':25},'secondary':{'usedPercent':50}}}
        print(json.dumps({'id':msg['id'],'result':result}),flush=True)
''',
    }
    for name, text in wrappers.items():
        path = bindir / name
        path.write_text(text)
        path.chmod(0o755)
    env = dict(os.environ, HOME=str(home), PATH=f'{bindir}:/usr/bin:/bin', LANG='C.UTF-8')
    subprocess.run(['bash', 'install.sh'], cwd=source, env=env, check=True)
    assert (plugins / 'libcodex-monitor.so').is_file()
    installed = home / '.local/share/codex-monitor/codex-limits.py'
    # Simulate a panel session that lacks the CLI directory in PATH.
    output = subprocess.check_output(['/usr/bin/python3', str(installed), '--short'], env=dict(env, PATH='/usr/bin:/bin'), text=True)
    assert output.strip() == 'Codex 5h 75% | 7d 50%', output
    subprocess.run(['bash', 'uninstall.sh'], cwd=source, env=env, check=True)
    subprocess.run(['bash', 'uninstall.sh'], cwd=source, env=env, check=True)
    assert not (plugins / 'libcodex-monitor.so').exists()
    assert not installed.exists()
    assert not (home / '.local/bin/codex-limits').exists()
    print('PASS: isolated install, desktop PATH, uninstall and repeated uninstall')
