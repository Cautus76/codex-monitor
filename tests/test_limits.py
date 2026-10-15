import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('limits', Path(__file__).resolve().parents[1] / 'codex-limits.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class LimitsTests(unittest.TestCase):
    def run_cli(self, data, *args):
        out = io.StringIO()
        with patch.object(m, 'query', return_value=data), patch('sys.argv', ['codex-limits', *args]), contextlib.redirect_stdout(out), patch.object(m.time, 'time', return_value=1000):
            status = m.main()
        return status, out.getvalue()

    def test_countdown_rounds_up_and_preserves_layout(self):
        status, output = self.run_cli({'primary': {'usedPercent': 37, 'resetsAt': 4600.1}, 'secondary': {'usedPercent': 38}}, '--short')
        self.assertEqual(status, 0)
        self.assertEqual(output.strip(), 'Codex 5h 63% (reset 1h 01m) | 7d 62%')

    def test_expired_reset_and_clamped_values(self):
        status, output = self.run_cli({'primary': {'usedPercent': 110, 'resetsAt': 999}, 'secondary': {'usedPercent': -10}}, '--short')
        self.assertEqual(status, 0)
        self.assertIn('5h 0% (reset 0h 00m) | 7d 100%', output)

    def test_missing_primary(self):
        self.assertEqual(self.run_cli({'secondary': {'usedPercent': 25}}, '--short'), (0, 'Codex 7d 75%\n'))

    def test_json_window_duration(self):
        status, output = self.run_cli({'primary': {'usedPercent': 20, 'windowDurationMins': 300, 'resetsAt': 4600}}, '--json')
        data = json.loads(output)
        self.assertEqual(status, 0)
        self.assertEqual(data['limits']['primary'], {'left_percent': 80, 'window_minutes': 300, 'resets_at': 4600})

    def test_invalid_data(self):
        for data in ({}, {'primary': {'usedPercent': float('nan')}}, {'primary': {'usedPercent': 1, 'resetsAt': 'bad'}}):
            status, output = self.run_cli(data, '--json')
            self.assertEqual(status, 1)
            self.assertFalse(json.loads(output)['ok'])

    def test_languages(self):
        with patch.dict(os.environ, {'LC_ALL': '', 'LC_MESSAGES': 'cs_CZ.UTF-8'}):
            self.assertEqual(m.language('auto'), 'cs')
        self.assertIn('zbývá', self.run_cli({'primary': {'usedPercent': 10}}, '--lang', 'cs')[1])

    def test_rpc_transport_and_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / 'codex'
            fake.write_text('''#!/usr/bin/python3
import json, sys
for line in sys.stdin:
    msg = json.loads(line)
    if msg.get('id') == 1:
        print('invalid json', flush=True)
        print(json.dumps({'method':'notification'}), flush=True)
        print(json.dumps({'id':1,'result':{}}), flush=True)
    if msg.get('id') == 2:
        print(json.dumps({'id':2,'result':{'rateLimits':{'primary':{'usedPercent':23}}}}), flush=True)
''')
            fake.chmod(0o755)
            with patch.object(m, 'codex_executable', return_value=str(fake)):
                self.assertEqual(m.query()['primary']['usedPercent'], 23)
            fake.write_text('#!/usr/bin/python3\nimport time\ntime.sleep(10)\n')
            with patch.object(m, 'codex_executable', return_value=str(fake)), self.assertRaises(TimeoutError):
                m.query(timeout=0.05)
            fake.write_text('#!/usr/bin/python3\n')
            with patch.object(m, 'codex_executable', return_value=str(fake)), self.assertRaises(RuntimeError):
                m.query()


if __name__ == '__main__':
    unittest.main()
