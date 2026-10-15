# Release validation: 1.0.0-rc.1

Validated on 2026-10-15 using elementary OS 8.1, Wingpanel 8.0.4, Vala 0.56.17 and Codex CLI 0.162.1.

- Existing installed helper matched the working local helper. Existing installed module matched the prior local build by SHA-256. Neither installed file was replaced or removed.
- Release work started from the latest fetched origin/main in a separate worktree; existing local changes and backup files were left intact.
- Indicator.vala is unchanged, preserving layout, worker-thread queries, overlap prevention, startup/open refresh and the 60-second timer.
- Seven Python regression tests cover countdown rounding, elapsed resets, clamping, missing windows, malformed values, locale selection, newline-delimited RPC notifications, timeout, early server exit and process cleanup.
- Python compilation and Bash syntax validation passed.
- Isolated installer test builds the real module using system development packages, installs into temporary user/plugin directories, checks the saved CLI path with a restricted desktop PATH, uninstalls and repeats uninstallation. Codex and sudo are test doubles. It does not exercise actual apt downloads, sudo authentication or a display session.
- Real-account stdio requests returned both primary and secondary limits. No raw account response or private usage values are included in this report.
- Vala compilation succeeds with a warning in generated C about GLib volatile atomic types; no source-level Vala errors. The module exports get_indicator.
- Public source/history and release archive were checked for credentials, private paths, authentication files and accidental build/backup artifacts. The original MIT license is retained. No additional runtime dependencies were introduced.

## Before a stable v1.0.0

The user previously confirmed the original installed indicator works. There is no running Wingpanel process in this validation session. Direct visual testing and loading this newly packaged helper in a running panel were therefore not performed. Do not replace that missing evidence with compilation results.

Install rc.1 in a normal Pantheon session, log out/in, verify both percentages and countdown against the CLI, wait through refresh, test an offline/recovery cycle, and repeat installation on a clean supported machine. Until then this is explicitly a prerelease.
