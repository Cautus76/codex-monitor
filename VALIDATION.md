# Release validation: 1.0.0-rc.1

Initial automated and isolated validation on 2026-10-15 using elementary OS 8.1, Wingpanel 8.0.4, Vala 0.56.17 and Codex CLI 0.162.1.

- Existing installed helper matched the working local helper. Existing installed module matched the prior local build by SHA-256. Neither installed file was replaced or removed.
- Release work started from the latest fetched origin/main in a separate worktree; existing local changes and backup files were left intact.
- Indicator.vala is unchanged, preserving layout, worker-thread queries, overlap prevention, startup/open refresh and the 60-second timer.
- Seven Python regression tests cover countdown rounding, elapsed resets, clamping, missing windows, malformed values, locale selection, newline-delimited RPC notifications, timeout, early server exit and process cleanup.
- Python compilation and Bash syntax validation passed.
- Isolated installer test builds the real module using system development packages, installs into temporary user/plugin directories, checks the saved CLI path with a restricted desktop PATH, uninstalls and repeats uninstallation. Codex and sudo are test doubles. It does not exercise actual apt downloads, sudo authentication or a display session.
- Real-account stdio requests returned both primary and secondary limits. No raw account response or private usage values are included in this report.
- Vala compilation succeeds with a warning in generated C about GLib volatile atomic types; no source-level Vala errors. The module exports get_indicator.
- Public source/history and release archive were checked for credentials, private paths, authentication files and accidental build/backup artifacts. The original MIT license is retained. No additional runtime dependencies were introduced.

## Target-machine test reported on 2026-10-16

Source: the user's explicit test report for **v1.0.0-rc.1**, not a new automated or visual test performed by the release-preparation agent.

Hardware and environment: Mac mini 2014 running Linux, Pantheon and Wingpanel 8.0.4. This is a Linux installation on Apple hardware, not a macOS compatibility claim. The report did not specify the Linux distribution or CLI version for this test.

Confirmed by the user:

- All seven Python tests passed.
- The installer successfully built and installed the indicator.
- Live limits were retrieved through Codex App Server.
- The countdown until the 5-hour limit reset displayed correctly.
- After logout/login, the installed rc.1 indicator loaded successfully into Wingpanel.
- Displayed usage values matched the actual values according to the user.

This confirms the previously missing real-panel installation/loading check for rc.1 on the target computer. It does not establish a clean installation on a second computer. The report did not separately confirm a timed 60-second refresh observation or an offline/recovery cycle; those observations must not be inferred from it. The refresh implementation remains unchanged.

## Before a stable v1.0.0

**Outstanding release gate: clean installation on a second supported computer — unverified.** The target-machine test above does not satisfy this independent check.

Record that machine's environment and confirm source-archive installation without manual source edits, login, live limits, panel loading after logout/login and correct percentages/countdown. Also record an observed refresh interval and offline/recovery behavior, which were not explicitly covered in the target-machine report. See [RELEASE_PLAN.md](RELEASE_PLAN.md) for the checklist and draft stable release notes.

Keep v1.0.0-rc.1 marked as a prerelease. Do not create or publish the stable v1.0.0 tag/release or change the program version until the remaining validation has been completed and recorded.
