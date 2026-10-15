#!/usr/bin/env python3
"""Query the official Codex app-server for rate limits; never handle credentials."""
import argparse
import json
import os
import select
import subprocess
import sys
import time
from datetime import datetime


def language(choice):
    return choice if choice != 'auto' else ('cs' if os.environ.get('LC_ALL', os.environ.get('LANG', '')).lower().startswith('cs') else 'en')


def query(timeout=20):
    process = subprocess.Popen(['codex', 'app-server', '--stdio'], stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=0)
    pending = b''
    deadline = time.monotonic() + timeout

    def send(data):
        process.stdin.write((json.dumps(data) + '\n').encode())
        process.stdin.flush()

    def receive(request_id):
        nonlocal pending
        while time.monotonic() < deadline:
            while b'\n' in pending:
                row, pending = pending.split(b'\n', 1)
                try:
                    reply = json.loads(row)
                except (ValueError, UnicodeError):
                    continue
                if reply.get('id') == request_id:
                    if 'error' in reply:
                        raise RuntimeError(str(reply['error']))
                    return reply.get('result', {})
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            readable, _, _ = select.select([process.stdout], [], [], remaining)
            if not readable:
                break
            chunk = os.read(process.stdout.fileno(), 65536)
            if not chunk:
                raise RuntimeError('Codex app-server closed the connection')
            pending += chunk
        raise TimeoutError('Codex app-server timed out')

    try:
        send({'method': 'initialize', 'id': 1, 'params': {'clientInfo': {
            'name': 'codex_limits_monitor', 'title': 'Codex Limits Monitor', 'version': '0.2.0'}}})
        receive(1)
        send({'method': 'initialized'})
        send({'method': 'account/rateLimits/read', 'id': 2})
        response = receive(2)
        limits = response.get('rateLimits') or {}
        if not limits:
            raise ValueError('Empty rate limits response')
        return limits
    finally:
        process.terminate()
        try:
            process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate()


def main():
    parser = argparse.ArgumentParser(description='Codex rate limits / Limity Codexu')
    parser.add_argument('--lang', choices=['en', 'cs', 'auto'], default='auto')
    parser.add_argument('--json', action='store_true', help='Machine-readable output')
    parser.add_argument('--short', action='store_true', help='Single-line panel output')
    options = parser.parse_args()
    lang = language(options.lang)
    try:
        limits = query()
        result = {'ok': True, 'source': 'codex-app-server', 'queried_at': int(time.time()), 'limits': {}}
        for key in ('primary', 'secondary'):
            value = limits.get(key)
            if value and value.get('usedPercent') is not None:
                result['limits'][key] = {'left_percent': max(0, min(100, 100-float(value['usedPercent']))),
                                         'resets_at': value.get('resetsAt'), 'window_minutes': value.get('windowMinutes')}
        if not result['limits']:
            raise ValueError('No percentage values in response')
        if options.json:
            print(json.dumps(result, ensure_ascii=False))
        elif options.short:
            parts = [f"{label} {result['limits'][key]['left_percent']:.0f}%" for key, label in [('primary', '5h'), ('secondary', '7d')] if key in result['limits']]
            print('Codex ' + ' | '.join(parts))
        else:
            for key, title in [('primary', '5-hour limit' if lang == 'en' else 'Pětihodinový limit'),
                               ('secondary', 'Weekly limit' if lang == 'en' else 'Týdenní limit')]:
                if key not in result['limits']:
                    continue
                entry = result['limits'][key]
                print(f"{title}: {entry['left_percent']:.0f}% {'left' if lang == 'en' else 'zbývá'}")
                if entry['resets_at']:
                    stamp = datetime.fromtimestamp(entry['resets_at']).strftime('%d.%m.%Y %H:%M')
                    print(f"  {'Reset' if lang == 'en' else 'Obnovení'}: {stamp}")
    except Exception as exc:
        if options.json:
            print(json.dumps({'ok': False, 'source': 'codex-app-server', 'error': str(exc)}))
        else:
            print(('Codex: unavailable (' if lang == 'en' else 'Codex: nedostupný (') + str(exc) + ')', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
