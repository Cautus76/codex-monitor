# Stable v1.0.0 preparation — not released

Current program version and public release: **1.0.0-rc.1 (prerelease)**.
This document is preparation only, not evidence that the checks below have passed.
Runtime functionality and panel appearance remain unchanged.

## Evidence available

- Automated, compilation, isolated installation and real-account checks: see VALIDATION.md.
- User-reported target-machine rc.1 installation and panel loading on Linux / Pantheon / Wingpanel 8.0.4, including confirmed correct values and countdown: reported 2026-10-16.

## Remaining validation

- [ ] Test a clean source-archive installation on a **second supported computer**, without manually editing sources. This remains unverified.
- [ ] Record OS/distribution, Wingpanel, Python, Vala and Codex CLI versions, test date and whether build dependencies were initially missing. Do not record account identifiers or credentials.
- [ ] Confirm installer build/install, existing or official CLI login, live retrieval of both limits, and panel loading after logout/login on that computer.
- [ ] Compare both panel percentages and the 5-hour reset countdown with CLI results.
- [ ] Observe a refresh after approximately 60 seconds; verify unavailable state during an offline query and recovery after reconnecting. These were not explicitly confirmed in the target-machine report.
- [ ] Confirm uninstallation using the supplied script removes monitor files while preserving Codex CLI and authentication; reinstall if needed.
- [ ] Record the actual outcomes and any limitations in VALIDATION.md. Resolve release-blocking failures before proceeding.

## Publication steps after validation passes

1. Review the latest remote main without overwriting concurrent changes.
2. Change VERSION in codex-limits.py to 1.0.0; finalize the changelog, both READMEs and stable release notes with the actual release date and verified scope.
3. Run the documented Python, shell, build and isolated-install checks; verify live queries without publishing private output. Review the final diff and scan the tracked release contents for private data.
4. Build codex-monitor-1.0.0.tar.gz from the exact reviewed commit, including install.sh, uninstall.sh and LICENSE. Test extracted sources and generate SHA256SUMS.
5. Push the reviewed commit to main, tag that exact commit v1.0.0 and publish the stable GitHub release with archive and checksum only after the validation gate above is satisfied.
6. Download the published archive and verify its checksum. Preserve the existing rc.1 tag and assets as historical artifacts.

No stable tag, draft GitHub release or replacement rc.1 archive is created by this preparation.

## Draft stable release notes — use only after the gate passes

Codex Monitor v1.0.0 is an unofficial usage indicator for Linux with Pantheon / Wingpanel 8. It displays remaining 5-hour and weekly Codex quotas with a countdown to the 5-hour reset, refreshing asynchronously every 60 seconds and when opened. English and Czech terminal output and documentation are included. It uses the existing Codex CLI login and requires no additional Python packages or API key.

Install: extract codex-monitor-1.0.0.tar.gz, open a terminal in the extracted directory and run bash install.sh as your normal desktop user. Log out and back in. Uninstall with bash uninstall.sh. See the READMEs for development-package requirements and troubleshooting.

Validation: insert the actual second-machine test results and final release checks here after completion. Keep scope limited to tested environments; Apple hardware running Linux does not imply macOS support. The upstream app-server interface remains experimental.
