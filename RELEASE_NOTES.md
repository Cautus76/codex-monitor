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

**This is a prerelease:** the original indicator was confirmed working by its user, but loading this newly packaged version in a running Wingpanel and a clean second-machine installation could not be verified in this session. These checks remain before stable v1.0.0. The Codex app-server interface is experimental. See VALIDATION.md.

No account data, credentials or machine-specific paths are included in the release archive.
