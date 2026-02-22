# Autocommit Control

Autocommit now requires this flag file:

- `scripts/.autocommit-enabled`

If the file does not exist, these scripts exit without running Git commands:

- `scripts/watch_antigravity.ps1`
- `scripts/commit_all.ps1`

## Commands

Enable:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\enable_autocommit.ps1
```

Disable:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\disable_autocommit.ps1
```
