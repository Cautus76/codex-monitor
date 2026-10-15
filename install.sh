#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
LANG_CHOICE=en
[[ "${LC_ALL:-${LANG:-}}" == cs* ]] && LANG_CHOICE=cs
say(){ if [[ "$LANG_CHOICE" == cs ]]; then echo "$2"; else echo "$1"; fi; }
command -v apt-get >/dev/null || { say 'This installer supports Debian/Ubuntu-based distributions only.' 'Instalátor podporuje pouze systémy založené na Debianu/Ubuntu.'; exit 1; }
if ! command -v codex >/dev/null; then
  say 'Codex CLI is missing. Install it from the official OpenAI instructions, then rerun this script.' 'Codex CLI chybí. Nainstaluj ho podle oficiálního návodu OpenAI a spusť instalátor znovu.'
  echo 'https://developers.openai.com/codex/cli/'
  exit 1
fi
if ! codex app-server --help >/dev/null 2>&1; then
  say 'Codex app-server is unavailable. Please update Codex CLI.' 'Codex app-server není dostupný. Aktualizuj Codex CLI.'; exit 1
fi
if ! codex login status 2>&1 | grep -q 'Logged in'; then
  say 'Codex login required; launching official login.' 'Je potřeba přihlášení do Codexu; spouštím oficiální přihlášení.'
  codex login
fi
missing=()
for cmd in valac pkg-config python3; do command -v "$cmd" >/dev/null || missing+=("$cmd"); done
if ! pkg-config --exists wingpanel gtk+-3.0 gmodule-2.0 2>/dev/null || ((${#missing[@]})); then
  say 'Missing build dependencies. Install using apt?' 'Chybí sestavovací závislosti. Nainstalovat pomocí apt?'
  read -r -p '[y/N] ' answer
  [[ "${answer,,}" == y || "${answer,,}" == a ]] || exit 1
  sudo apt-get update
  sudo apt-get install -y valac pkg-config libwingpanel-dev libgtk-3-dev libglib2.0-dev python3
fi
if ! pkg-config --exists wingpanel gtk+-3.0 gmodule-2.0; then
  say 'Wingpanel development packages not found. Pantheon Wingpanel 8 is required.' 'Nenalezeny vývojové balíčky Wingpanelu. Je vyžadován Pantheon Wingpanel 8.'; exit 1
fi
libdir="$(pkg-config --variable=indicatorsdir wingpanel)"
[[ -n "$libdir" && -d "$libdir" ]] || { say 'Wingpanel plugin directory not found.' 'Složka pluginů Wingpanelu nenalezena.'; exit 1; }
mkdir -p build "$HOME/.local/share/codex-monitor" "$HOME/.local/bin"
say 'Building Wingpanel module…' 'Sestavuji modul Wingpanelu…'
valac --library=codex-monitor --pkg wingpanel --pkg gtk+-3.0 --pkg gmodule-2.0 -X -fPIC -X -shared -o build/libcodex-monitor.so Indicator.vala
install -m 755 codex-limits.py "$HOME/.local/share/codex-monitor/codex-limits.py"
ln -sfn "$HOME/.local/share/codex-monitor/codex-limits.py" "$HOME/.local/bin/codex-limits"
say 'Checking live limits…' 'Kontroluji živé limity…'
"$HOME/.local/bin/codex-limits" || say 'Live query failed; check your Codex login/network.' 'Živý dotaz selhal; zkontroluj přihlášení a síť.'
if [[ -f "$libdir/libcodex-limits.so" ]]; then
  say 'Old prototype detected. Remove the old plugin after verifying this version, to avoid duplicate indicators.' 'Nalezena stará testovací verze. Po ověření nové odeber starý plugin, aby nevznikly dva indikátory.'
fi
say 'Installing Wingpanel module (administrator permission required)…' 'Instaluji modul Wingpanelu (vyžaduje oprávnění správce)…'
sudo install -m 644 build/libcodex-monitor.so "$libdir/libcodex-monitor.so"
say 'Installation complete. Log out and log back in to load the indicator.' 'Instalace hotová. Odhlas se a znovu přihlas pro načtení indikátoru.'
