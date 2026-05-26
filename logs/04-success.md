# Success — both packages install cleanly

**Date:** 2026-05-26
**Bundle version:** v0.3.0 (all fixes applied)
**Target:** Windows 10, Python 3.13.13, `win_amd64`

## Log

```
F:\packages portapkg\UI_53sksy_2026-05-26>python portapkg.py install --all

---

Installing auto-py-to-exe...
  Platform: win_amd64
  Python:   313
  Wheels:   28 compatible found
  Looking in links: ...\bundles\auto-py-to-exe\wheels
  Processing ...\auto-py-to-exe-2.50.1-py3-none-any.whl
  Processing ...\pefile-2024.8.26-py3-none-any.whl
  Processing ...\pywin32-ctypes-0.2.3-py3-none-any.whl
  Processing ...\cffi-2.0.0-cp313-cp313-win_amd64.whl
  Processing ...\pycparser-3.0-py3-none-any.whl
  ... (all 28 wheels resolved)
  Successfully installed auto-py-to-exe

---

Installing flet...
  Wheels:   11 compatible found
  Processing ...\flet-0.85.2-py3-none-any.whl
  Processing ...\msgpack-1.1.2-cp313-cp313-win_amd64.whl
  ... (all 11 wheels resolved)
  Successfully installed flet

---

All packages installed successfully.
```

## What changed

| Layer | What it fixes | Packages affected |
|---|---|---|
| **Fetch Layer 3** — unconstrained sdist | Packages with zero binary wheels (sdist-only) | `eel`, `bottle-websocket` |
| **Fetch Layer 4** — version bump | Packages whose resolved version is missing newer-Python wheels | `msgpack` (when cp313 wheels weren't available) |
| **Resolve — platform-conditional METADATA scan** | Deps gated on `sys_platform == "win32"` not seen on macOS host | `pefile`, `pywin32-ctypes`, `cffi` |
| **Resolve — recursive tree resolution** | Transitive conditional deps (dep of a dep) | `pycparser` (from `cffi`) |
