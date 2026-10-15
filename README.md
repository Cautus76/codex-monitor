# Codex Monitor for Wingpanel

**English** · [Čeština](README.cs.md)

A small, unofficial live Codex usage monitor for **elementary OS / Pantheon Wingpanel 8**. Displays remaining 5-hour and weekly quotas in the top bar and provides a `codex-limits` terminal command. Refreshes every 60 seconds, using your existing Codex CLI ChatGPT login.

**Status: preview, needs testing on a real Pantheon installation.** Not affiliated with or endorsed by OpenAI or elementary.

## Requirements

- Linux distribution with Pantheon / Wingpanel 8 (tested target: Wingpanel 8.0.4; actual plugin loading must still be verified)
- Codex CLI with `codex app-server` and ChatGPT login (tested live-query protocol with Codex CLI 0.162.1)
- Python 3, Vala, GTK 3 and Wingpanel development headers for compilation
- Network connectivity for live usage information

No API key, `pipx`, or extra paid API access required. Login tokens are managed by Codex CLI, not this project.

## Install

```bash
bash install.sh
```

The installer checks Codex and Wingpanel, prompts before installing missing build dependencies via `apt`, offers official Codex login when needed, compiles the indicator and installs it using `sudo` only for the Wingpanel system library. Log out and log back in afterwards.

The installer currently targets Debian/Ubuntu-based systems. Other desktops (KDE, GNOME, XFCE) are **not** supported by this Wingpanel plugin.

## Verify

```bash
codex login status
codex-limits
codex-limits --json
file build/libcodex-monitor.so
nm -D build/libcodex-monitor.so | grep get_indicator
```

Example (not live data):

```text
5-hour limit: 0% left
  Reset: 15.10.2026 21:40
Weekly limit: 68% left
  Reset: 22.10.2026 11:09
```

Check installation path using:

```bash
pkg-config --variable=indicatorsdir wingpanel
```

The top-panel indicator may require logout/login to load. Compilation success alone does not prove it loaded. If the panel does not appear, inspect `journalctl --user` and Wingpanel startup logs.

## Uninstall

From the project folder:

```bash
bash uninstall.sh
```

Log out and log back in to unload the removed plugin. Uninstallation does **not** remove Codex CLI, your authentication or system build tools.

## Languages

- English: default
- Czech: automatically when `LANG`/`LC_ALL` starts with `cs`

For terminal override use `codex-limits --lang en` or `codex-limits --lang cs`.

## Notes and limits

- Queries `account/rateLimits/read` through `codex app-server --stdio` with the existing CLI login. It does not read or publish `~/.codex/auth.json`.
- If offline or unauthenticated, displays an unavailable state rather than stale numbers.
- Query every 60 seconds when loaded in the panel. The remote API and CLI behavior may change across Codex versions.
- Never run unknown installation scripts without reviewing them first.
