# Third attempt — pycparser still missing

**Date:** 2026-05-26
**Bundle version:** v0.2.0 + platform-aware resolver (but buggy marker eval)
**Target:** Windows 10, Python 3.13.13, `win_amd64`

## Log

```
F:\packages portapkg\UI_6a7f27_2026-05-26>python portapkg.py install --all

---

Installing auto-py-to-exe...
  Wheels:   27 compatible found
  ERROR: Could not find a version that satisfies the requirement
         pycparser; implementation_name != "PyPy" (from cffi)
         No matching distribution found for pycparser; implementation_name != "PyPy"

Installing flet...
  Already installed. (from previous run)
```

## Analysis

| Issue | Root cause |
|---|---|
| `pycparser` missing | `cffi` (a newly-resolved conditional dep of `gevent` on win32) requires `pycparser`. The scanner found `cffi` via `sys_platform` check, but didn't recursively scan `cffi`'s own METADATA. |
| `pycparser` condition `implementation_name != "PyPy"` | The marker evaluator used `.strip('"')` which tore off the closing quote of `"win32"`, silently breaking marker evaluation. All conditionals evaluated to False. |
| Only top-level conditionals checked | The scanner only looked at the top-level package's deps, not at newly-resolved transitive deps. |

## Fixes applied

1. **Recursive conditional scan** (`resolver.py`): `_resolve_conditional_tree()` loops until the dep set stabilizes, downloading each new dep and re-scanning its METADATA.
2. **Proper marker evaluation** (`resolver.py`): Removed `.strip('"')` from `_conditional_matches_platform`. Now uses `pip._vendor.packaging.markers.Marker` directly.
3. **RFC 822 line unfolding** (`resolver.py`): Added `_unfold_metadata()` to handle folded METADATA lines (continuation with leading whitespace).
