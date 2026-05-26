# CLI reference

## `portapkg`

The main CLI for bundling packages on an online machine.

### Commands

#### `portapkg bundle <package>`

Bundle a package for offline install.

```bash
portapkg bundle instrumation
portapkg bundle instrumation --platforms win_amd64,macosx_13_0_arm64
portapkg bundle instrumation --snapshot
```

**Options:**

| Flag | Description |
|---|---|
| `package` | Package name (positional, required) |
| `--platforms` | Comma-separated platform tags (default: all 6) |
| `--snapshot` | Snapshot current environment (single-platform) |

#### `portapkg list`

List all bundles in the bundles directory.

```bash
portapkg list
```

#### `portapkg info <package>`

Show details about a specific bundle.

```bash
portapkg info instrumation
```

#### `portapkg export [package]`

Export one or more bundles + standalone installer into a portable folder.

```bash
# Single package (positional)
portapkg export instrumation

# Multiple packages with custom name
portapkg export --name mydev --packages pyserial,pyvisa,pyvisa-py

# Auto-generated name for multiple packages
portapkg export --packages pyserial,pyvisa

# To a specific directory
portapkg export instrumation --output ./dist
```

Creates `{name}_{random_id}_{date}/` with `portapkg.py` + `bundles/{package(s)}/`
inside — ready to ship.

**Options:**

| Flag | Description |
|---|---|
| `package` | Package name (positional, optional if `--packages` used) |
| `--name` | Custom export folder name (default: package name or `"bundle"`) |
| `--packages` | Comma-separated list of packages to include |
| `--output`, `-o` | Output directory (default: current directory) |

#### `portapkg update <package>`

Re-fetch a bundle (same options as `bundle`).

```bash
portapkg update instrumation
portapkg update instrumation --platforms win_amd64
portapkg update instrumation --snapshot
```

**Options:**

| Flag | Description |
|---|---|
| `package` | Package name (positional, required) |
| `--platforms` | Comma-separated platform tags |
| `--snapshot` | Snapshot mode |

### Global options

- `PORTAPKG_BUNDLES_DIR` environment variable overrides the bundle directory

---

## `portapkg.py`

The standalone script — works for **both bundling and installing** on any
machine with Python and pip. No `pip install portapkg` needed.

### Commands

#### `python portapkg.py bundle <package>`

Bundle a package (same options as the CLI).

```bash
python portapkg.py bundle instrumation
python portapkg.py bundle instrumation --platforms win_amd64,macosx_13_0_arm64
python portapkg.py bundle instrumation --snapshot
```

#### `python portapkg.py export [package]`

Export one or more bundles into a portable folder.

```bash
# Single package
python portapkg.py export instrumation

# Multiple packages with custom name
python portapkg.py export --name mydev --packages pyserial,pyvisa

# To a specific directory
python portapkg.py export instrumation --output ./dist
```

#### `python portapkg.py install <package>`

Install a bundled package.

```bash
python portapkg.py install instrumation
python portapkg.py install instrumation --target ./venv/Lib/site-packages
```

**Options:**

| Flag | Description |
|---|---|
| `package` | Package name (positional, required) |
| `--target` | Custom install path |

#### `python portapkg.py list`

List available bundles.

```bash
python portapkg.py list
```

### Global options

- `PORTAPKG_BUNDLES_DIR` environment variable overrides the bundle directory
