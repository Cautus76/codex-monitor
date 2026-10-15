#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
libdir="$(pkg-config --variable=indicatorsdir wingpanel 2>/dev/null || true)"
if [[ -z "$libdir" ]]; then
  libdir='/usr/lib/x86_64-linux-gnu/wingpanel'
fi
if [[ -f "$libdir/libcodex-monitor.so" ]]; then
  sudo rm -- "$libdir/libcodex-monitor.so"
fi
rm -f "$HOME/.local/bin/codex-limits"
rm -f "$HOME/.local/share/codex-monitor/codex-limits.py"
rmdir "$HOME/.local/share/codex-monitor" 2>/dev/null || true
printf 'Codex Monitor removed / Codex Monitor odstraněn. Log out and back in / Odhlas se a znovu přihlas.\n'
