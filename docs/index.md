# portapkg

**Portable, offline-friendly Python package bundler and installer.**

Bundle a package and all its dependencies on an online machine, then install
on an air-gapped machine with nothing but Python and pip.

## Why portapkg?

- **No server needed** — bundles are plain folders you can copy on a USB drive
- **Multi-platform** — one bundle works across Windows, Linux, macOS, x86, and ARM
- **Self-contained** — the standalone `portapkg.py` is stdlib only, no dependencies
- **Works offline** — `pip install --no-index --find-links` under the hood

## Quick start

### On an online machine

```bash
pip install portapkg
portapkg bundle instrumation
```

This creates a `bundles/` folder with wheels for all 6 platforms × 5 Python versions.

### On an offline machine

Copy `bundles/` and `portapkg.py` to a USB drive, then run:

```bash
python portapkg.py list
python portapkg.py install instrumation
```

## How it works

1. **Dependency resolution**: `pip download <package>` resolves the full
   transitive dependency tree using pip's own resolver.
2. **Multi-platform fetch**: For each dependency, wheels are downloaded
   across 6 platforms × 5 Python versions.
3. **Fallback**: If no binary wheel exists for a platform, it falls
   back to a source distribution with a warning.
4. **Offline install**: `pip install --no-index --find-links <wheels_dir>`
   installs from local files only.

## Next steps

- [Usage guide](usage.md) — detailed CLI and standalone instructions
- [Configuration](configuration.md) — environment variables and options
- [CLI reference](cli.md) — full command reference
- [Development](development.md) — contributing, testing, project structure
