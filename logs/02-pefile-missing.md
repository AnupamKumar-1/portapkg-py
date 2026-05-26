# Second attempt — pefile still missing

**Date:** 2026-05-26
**Bundle version:** v0.2.0 + fetch.py layered fallback
**Target:** Windows 10, Python 3.13.13, `win_amd64`

## Log

```
F:\packages portapkg\UI_rw3n7x_2026-05-26>python portapkg.py install --all

---

Installing auto-py-to-exe...
  Wheels:   23 compatible found
  ERROR: Could not find a version that satisfies the requirement
         pefile>=2022.5.30; sys_platform == "win32" (from pyinstaller)
         No matching distribution found for pefile>=2022.5.30

Installing flet...
  Wheels:   11 compatible found
  Successfully installed flet  (all 11 wheels resolved)
```

## Analysis

| Issue | Root cause |
|---|---|
| `pefile` missing | Conditional dependency `pefile>=2022.5.30; sys_platform == "win32"` is skipped by `pip download` when running on macOS (host machine). The resolver never included it in the dependency list. |
| `pywin32-ctypes` also missing | Same root cause — another `sys_platform == "win32"` conditional from `pyinstaller`. |

## Fixes applied

1. **Platform-aware resolution** (`resolver.py`): Added `--platform win_amd64` to `pip download` in the resolver to force resolution of platform-conditional deps.
2. **METADATA scanning** (`resolver.py`): After native resolution, scan all downloaded wheels' `METADATA` for `Requires-Dist` lines with platform conditionals. Add matching deps to the dependency list.
