# Initial bundle — all packages failed

**Date:** 2026-05-26
**Bundle version:** v0.2.0
**Target:** Windows 10, Python 3.13.13, `win_amd64`

## Log

```
Microsoft Windows [Version 10.0.18362.145]
F:\mystack_r0s6t6_2026-05-26>python portapkg.py install --all

---

Installing auto-py-to-exe...
  Wheels:   40 compatible found
  ERROR: Could not find a version that satisfies the requirement
         Eel!=0.18.0,>=0.11.0 (from auto-py-to-exe)
         No matching distribution found for Eel!=0.18.0,>=0.11.0

Installing flet...
  Wheels:   20 compatible found
  ERROR: Could not find a version that satisfies the requirement
         msgpack>=1.1.0 (from flet)
         No matching distribution found for msgpack>=1.1.0

Installing pyserial...
  Successfully installed pyserial-3.5

Installing pyvisa...
  Successfully installed pyvisa-1.16.2 typing_extensions-4.15.0

Installing pyvisa-py...
  Successfully installed pyvisa-py-0.8.1
```

## Analysis

| Issue | Root cause |
|---|---|
| `Eel` missing | Bundler's `download_wheels` couldn't find binary wheels for `Eel`. The existing sdist fallback still used `--platform`/`--python-version` flags which restricted resolution. |
| `msgpack` only had cp39 wheels | No Python 3.13 wheel existed for `msgpack==1.1.2` at the time. Bundler had no version-bump fallback. |

## Fixes applied

1. **Layered sdist fallback** (`fetch.py`): Added unconstrained `pip download --no-binary :all:` as Layer 3 when platform-constrained download fails.
2. **Version bump** (`fetch.py`): Added `_try_newer_version()` as Layer 4 — queries `pip index versions` and tries newer releases with binary wheels.
