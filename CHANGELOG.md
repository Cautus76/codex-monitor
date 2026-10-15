# Changelog

## 1.0.0-rc.1 — 2026-10-15

First packaged public prerelease, preserving the previously working Wingpanel appearance.

- Retain remaining 5-hour and weekly percentages, the 5-hour reset countdown and asynchronous 60-second refresh.
- Fix countdown rounding near minute boundaries and empty locale overrides.
- Save the installed CLI path so a desktop session can find Codex independently of its PATH.
- Validate non-finite percentages and malformed reset timestamps; bound incomplete protocol messages.
- Avoid exposing app-server error payloads; keep timeout and child-process cleanup.
- Correct JSON window duration parsing to use `windowDurationMins` from the current CLI schema.
- Check live limits before replacing installed files; detect missing C compiler and refuse installation as root.
- Record the module directory for portable uninstallation without a hardcoded architecture.
- Add English/Czech installation, troubleshooting and privacy documentation, regression tests and an isolated install/uninstall test.

### Verification and release status

Python regression tests, shell syntax, real Vala compilation, isolated install/uninstall and real-account queries passed on elementary OS 8.1 / Wingpanel 8.0.4 / Codex CLI 0.162.1. The original working installation was not modified. Loading the new release in a running Wingpanel and installation on a second clean machine remain to be verified; hence **rc.1**, not stable v1.0.0. See VALIDATION.md.

## Earlier preview — 2026-10-15

- Initial unofficial Wingpanel monitor with English/Czech terminal output.
- Added the 5-hour reset countdown and documented the user's successful panel test.
- Targeted Pantheon / Wingpanel 8 using the existing Codex CLI ChatGPT login.
