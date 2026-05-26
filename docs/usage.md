# Usage guide

## Installing portapkg

### From PyPI (recommended)

```bash
pip install portapkg
```

### From source

```bash
git clone https://github.com/abduznik/portapkg-py
cd portapkg-py
pip install -e ".[dev]"
```

### No install needed (standalone)

The `portapkg.py` file is fully self-contained — stdlib only. Just copy it
alongside your `bundles/` folder and you're ready.

## Bundling packages

### Basic bundling

```bash
portapkg bundle instrumation
```

This downloads wheels for **6 platforms × 5 Python versions** (up to 30
downloads per dependency). The output goes to `./bundles/instrumation/`.

### Specific platforms

```bash
portapkg bundle pyserial --platforms win_amd64,macosx_13_0_arm64
```

Valid platform tags:

| Platform | Tag |
|---|---|
| Windows x86_64 | `win_amd64` |
| Windows x86 | `win32` |
| Linux x86_64 | `manylinux2014_x86_64` |
| Linux ARM64 | `manylinux2014_aarch64` |
| macOS Apple Silicon | `macosx_13_0_arm64` |
| macOS Intel | `macosx_13_0_x86_64` |

### Snapshot mode (single platform)

```bash
portapkg bundle instrumation --snapshot
```

Downloads wheels for your **current machine only**. Faster and more reliable,
but the bundle only works on machines with the same OS and architecture.

### Custom bundle directory

```bash
PORTAPKG_BUNDLES_DIR=/path/to/bundles portapkg bundle instrumation
```

### List and inspect bundles

```bash
# List all bundles
portapkg list

# Show details of a specific bundle
portapkg info instrumation
```

### Update a bundle

```bash
# Re-fetch a bundle with all platforms
portapkg update instrumation

# Re-fetch with specific platforms
portapkg update instrumation --platforms win_amd64,linux_x86_64

# Re-fetch as snapshot
portapkg update instrumation --snapshot
```

## Installing offline

Copy the `bundles/` folder and `portapkg.py` to the offline machine.

### List available bundles

```bash
python portapkg.py list
```

### Install a bundled package

```bash
python portapkg.py install instrumation
```

### Install to a custom path

```bash
python portapkg.py install instrumation --target ./venv/Lib/site-packages
```

### Custom bundle directory

```bash
PORTAPKG_BUNDLES_DIR=/path/to/bundles python portapkg.py list
PORTAPKG_BUNDLES_DIR=/path/to/bundles python portapkg.py install instrumation
```

## Typical workflow

| Online machine | USB stick | Offline machine |
|---|---|---|
| `portapkg bundle pyserial` | `bundles/` folder | `python portapkg.py list` |
| `portapkg bundle pyvisa` | `portapkg.py` file | `python portapkg.py install pyserial` |
| → bundles ready in `./bundles/` | Copy both | → installs from local wheels |
