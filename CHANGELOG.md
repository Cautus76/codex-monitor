# Changelog

## Unreleased — stable v1.0.0 preparation

- Record the user's successful rc.1 test on a Mac mini 2014 running Linux, Pantheon and Wingpanel 8.0.4, reported on 2026-10-16: seven passing Python tests, successful build/install, live limits, correct reset countdown, panel loading after logout/login and confirmed displayed values.
- Update English/Czech documentation and prepare a stable-release checklist and draft notes.
- No runtime, installer or visual changes; version remains 1.0.0-rc.1.
- Clean installation on a second computer remains unverified. Stable v1.0.0 has not been approved or published.

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

Python regression tests, shell syntax, real Vala compilation, isolated install/uninstall and real-account queries passed on elementary OS 8.1 / Wingpanel 8.0.4 / Codex CLI 0.162.1. The original working installation was not modified. At publication, loading the new release in a running Wingpanel and installation on a second clean machine remained unverified. The subsequent target-machine report confirms panel loading; the second-machine clean installation remains outstanding. The release remains **rc.1**, not stable v1.0.0. See VALIDATION.md.

## Earlier preview — 2026-10-15

- Initial unofficial Wingpanel monitor with English/Czech terminal output.
- Added the 5-hour reset countdown and documented the user's successful panel test.
- Targeted Pantheon / Wingpanel 8 using the existing Codex CLI ChatGPT login.
