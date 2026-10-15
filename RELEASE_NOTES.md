# Codex Monitor v1.0.0-rc.1

First packaged public prerelease for elementary OS / Pantheon Wingpanel 8.

- Remaining 5-hour and weekly Codex quotas in the panel, with a 5-hour reset countdown.
- Asynchronous refresh every 60 seconds and on menu opening.
- Existing working appearance preserved.
- Improved CLI discovery in desktop sessions, response validation, timeout handling and installer checks.
- English and Czech setup, uninstall, troubleshooting and privacy documentation.
- MIT license; no additional Python runtime packages or API key required.

## Install

Download `codex-monitor-1.0.0-rc.1.tar.gz`, extract it, open a terminal in the extracted directory and run `bash install.sh` as your normal desktop user. The installer requests sudo when required. Log out and back in afterwards. See README.md or README.cs.md for requirements. Uninstall with `bash uninstall.sh`.

The archive contains sources and the installer; the module is compiled against your system's Wingpanel. `SHA256SUMS` verifies the archive download.

## Validation and prerelease status

Passed seven Python regression tests, Python and shell syntax checks, actual Vala compilation, isolated install/uninstall including restricted desktop PATH, and live Codex rate-limit queries on elementary OS 8.1 / Wingpanel 8.0.4 / Codex CLI 0.162.1. Existing installed files were preserved.

**Target-machine update, reported 16 October 2026:** the user successfully tested rc.1 on a Mac mini 2014 running Linux, Pantheon and Wingpanel 8.0.4. All seven Python tests passed; installation, live queries, reset countdown and loading into Wingpanel after logout/login worked. The user confirmed that displayed values were correct.

**This remains a prerelease:** a clean installation on a second computer is still unverified and is required before stable v1.0.0. The report did not separately confirm timed refresh or offline/recovery behavior. The Codex app-server interface is experimental. See the current [VALIDATION.md](https://github.com/Cautus76/codex-monitor/blob/main/VALIDATION.md) and [stable release preparation](https://github.com/Cautus76/codex-monitor/blob/main/RELEASE_PLAN.md).

This documentation update does not change the rc.1 tag, program version or downloadable archive/checksum.

No account data, credentials or machine-specific paths are included in the release archive.
