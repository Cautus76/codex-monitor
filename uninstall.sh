#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ "${EUID}" == 0 ]]; then
  echo 'Run as your desktop user, without sudo.' >&2
  exit 1
fi
libdir="$(pkg-config --variable=indicatorsdir wingpanel 2>/dev/null || true)"
if [[ -f "$HOME/.local/share/codex-monitor/indicators-dir" ]]; then
  libdir="$(cat "$HOME/.local/share/codex-monitor/indicators-dir")"
fi
[[ "$libdir" == /* && "$libdir" != / && "$libdir" != *..* ]] || {
  echo 'Cannot determine Wingpanel directory; install libwingpanel-dev and retry.' >&2
  exit 1
}
if [[ -f "$libdir/libcodex-monitor.so" ]]; then
  sudo rm -- "$libdir/libcodex-monitor.so"
fi
rm -f "$HOME/.local/bin/codex-limits"
rm -f "$HOME/.local/share/codex-monitor/codex-limits.py" \
  "$HOME/.local/share/codex-monitor/codex-path" \
  "$HOME/.local/share/codex-monitor/indicators-dir"
rmdir "$HOME/.local/share/codex-monitor" 2>/dev/null || true
printf 'Codex Monitor removed / Codex Monitor odstraněn. Log out and back in / Odhlas se a znovu přihlas.\n'
