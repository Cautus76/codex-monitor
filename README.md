# Codex Monitor for Wingpanel

**English** · [Čeština](README.cs.md)

An unofficial Codex usage indicator for elementary OS / Pantheon Wingpanel 8.
Shows the remaining 5-hour and weekly quotas, plus the time until the 5-hour reset:

```text
Codex 5h 63% (reset 3h 31m) | 7d 62%
```

Example values only. Percentages mean **remaining**, not used. The indicator refreshes on startup, when opened and every 60 seconds. Requests run in a worker thread and never overlap. No Python packages are required.

Version **1.0.0-rc.1** remains a public prerelease. On 16 October 2026, the user reported a successful test of this version on a Mac mini 2014 running Linux, Pantheon and Wingpanel 8.0.4: all seven Python tests passed, the installer built and installed the indicator, live limits and the reset countdown worked, and the indicator loaded after logout/login. The user confirmed the displayed values were correct. A clean installation on a second machine remains **unverified** and is required before stable v1.0.0. See [VALIDATION.md](VALIDATION.md) and the [stable release preparation](RELEASE_PLAN.md). Not affiliated with OpenAI or elementary.

## Requirements

- Linux with Pantheon and Wingpanel 8; this is not a macOS, GNOME, KDE or XFCE tray app.
- Debian/Ubuntu-based distribution for the supplied installer, with `apt-get` and `sudo`.
- [Official Codex CLI](https://developers.openai.com/codex/cli/) on your terminal's `PATH`, logged in with a ChatGPT account that provides Codex rate limits. API-key-only accounts may not expose these quotas.
- Python 3.8+, Bash, a C compiler, Vala, pkg-config, GTK 3, GLib and Wingpanel development files.
- Network access for live queries.

The installer offers to install missing build packages:

```bash
sudo apt-get install build-essential valac pkg-config libwingpanel-dev libgtk-3-dev libglib2.0-dev python3
```

Wingpanel development packages must be available in your distribution repositories. No API key, pip packages or additional paid API access are needed.

## Download and install

Download and extract the source archive from [Releases](https://github.com/Cautus76/codex-monitor/releases), open a terminal in the extracted folder, then run:

```bash
bash install.sh
```

Alternatively, with Git installed:

```bash
git clone https://github.com/Cautus76/codex-monitor.git
cd codex-monitor
bash install.sh
```

Run as your normal desktop user, **without `sudo`**. The installer offers the official `codex login` if needed, compiles the module, and checks live limits before replacing installed program files. It requests administrator access for packages and the system Wingpanel module. Log out and back in to load the indicator. Updates use the same procedure.

Installed files:

- `~/.local/share/codex-monitor/codex-limits.py`: helper actually used by the panel.
- `~/.local/share/codex-monitor/codex-path`: local CLI executable path, so terminal and desktop PATH differences do not break queries.
- `~/.local/share/codex-monitor/indicators-dir`: module directory recorded for uninstallation.
- `~/.local/bin/codex-limits`: terminal command symlink.
- `$(pkg-config --variable=indicatorsdir wingpanel)/libcodex-monitor.so`: system module.

Editing downloaded sources does not update the installed files. Rerun the installer after updating sources or moving the Codex CLI.

## Terminal usage

```bash
~/.local/bin/codex-limits
~/.local/bin/codex-limits --short
~/.local/bin/codex-limits --json
~/.local/bin/codex-limits --lang cs
~/.local/bin/codex-limits --version
```

Use `codex-limits` directly if `~/.local/bin` is on your PATH. English and Czech output are supported; helper language follows `LC_ALL`, `LC_MESSAGES`, then `LANG`. JSON includes remaining percentages, Unix reset timestamps and window durations in minutes when supplied by Codex. Detailed text prints reset times in your local timezone. The panel countdown rounds up to a minute and updates with each refresh, rather than every second. Elapsed reset timestamps display zero until the server supplies updated data.

## Uninstall

From the extracted or cloned project folder, as your normal user:

```bash
bash uninstall.sh
```

Log out and back in. This removes the module and helper files, leaving Codex CLI, its authentication and system build packages installed. A system module is shared across desktop users; removal affects all users of this module.

## Troubleshooting

- **Unavailable:** run `codex login status`, then `codex login` if needed. Check connectivity and run `python3 codex-limits.py --short`. Authentication, empty limits, server errors and a 20-second query timeout produce an unavailable state rather than stale percentages. A failed refresh retries on the next 60-second interval or when opened.
- **Terminal works, panel fails:** test `python3 ~/.local/share/codex-monitor/codex-limits.py --short`. Rerun the installer from a terminal where `codex` works to refresh the saved executable path. The CLI and its runtime (for example Node.js) must also work in the desktop session.
- **Command not found:** use `~/.local/bin/codex-limits`, or add `~/.local/bin` to your shell PATH.
- **No indicator:** log out and back in, check `pkg-config --variable=indicatorsdir wingpanel`, and inspect `journalctl --user -b` for Wingpanel errors. Successful compilation alone does not verify panel loading.
- **Missing Wingpanel headers:** install `libwingpanel-dev` from your distribution; another desktop panel cannot load this module.
- **Duplicate indicator:** an old `libcodex-limits.so` prototype may still exist. The installer warns about it but leaves it intact. Remove that old prototype only after identifying it.
- **CLI upgrade changes responses:** update Codex and this project together. The app-server interface is experimental. Include OS, Wingpanel and CLI versions in bug reports; redact private log content.

## Privacy and implementation

The helper uses the official [Codex app-server protocol](https://developers.openai.com/codex/app-server): initialize, initialized, then `account/rateLimits/read` over local stdio. It does not start inference turns or read authentication files. Codex CLI manages login and connects to OpenAI. The monitor stores no usage history or credentials, adds no telemetry, and does not expose the server over a network socket. Server error payloads are not echoed. Codex itself may retain logs according to its own settings.

Never commit login files, local CLI paths or real account output. See [LICENSE](LICENSE) (MIT) and [CHANGELOG.md](CHANGELOG.md).

## Development checks

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile codex-limits.py
bash -n install.sh uninstall.sh
python3 tests/install-smoke.py
python3 codex-limits.py --short
```

The smoke test needs build dependencies. It uses real Vala compilation, temporary HOME/plugin directories, a fake Codex server and a sudo wrapper, without changing the running installation. The final command is the separate real-account/network check; do not publish its output. See [VALIDATION.md](VALIDATION.md) for release evidence and remaining validation.
