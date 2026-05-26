# Exporting bundles

The `export` command packages a bundle and the standalone installer into
a single portable folder — ready to copy to a USB drive and ship.

## Why export?

Instead of manually copying `portapkg.py` and the `bundles/` directory, `export`
creates a tidy, timestamped folder that includes everything the offline machine
needs:

```
instrumation_a3f2e6_2026-05-26/
├── portapkg.py          ← standalone installer (stdlib only)
└── bundles/
    └── instrumation/
        ├── manifest.json
        └── wheels/
            └── ...
```

## Usage

You must have already [bundled](usage.md#bundling-packages) the package before
exporting it.

```bash
# Export a bundle for distribution
portapkg export instrumation

# Export to a specific directory
portapkg export instrumation --output ./dist
```

## How the folder is named

The export folder is named automatically as:

```
{package}_{short_id}_{today_date}
```

| Part | Description | Example |
|---|---|---|
| `package` | The package name | `instrumation` |
| `short_id` | A random 6-character hex string | `a3f2e6` |
| `today_date` | Today's date in ISO format | `2026-05-26` |

## What's inside

| File / folder | Purpose |
|---|---|
| `portapkg.py` | The standalone offline installer — no dependencies, stdlib only |
| `bundles/{package}/` | The bundle manifest and wheels |
| `bundles/{package}/manifest.json` | Metadata (version, deps, platform info) |
| `bundles/{package}/wheels/` | All downloaded wheel files |

## Using the exported folder on an offline machine

```bash
# Copy the entire folder to the offline machine, then:

cd instrumation_a3f2e6_2026-05-26/

# List available bundles
python portapkg.py list

# Install the package (no internet needed)
python portapkg.py install instrumation
```

## Using portapkg.py from source as an alternative

If you don't want to `pip install` portapkg on the online machine, you can
use the `portapkg.py` file directly from the source repository:

```bash
# Clone the repo
git clone https://github.com/abduznik/portapkg-py
cd portapkg-py

# Use the module directly (no pip install needed!)
python3 -m portapkg.cli bundle instrumation
python3 -m portapkg.cli list
python3 -m portapkg.cli info instrumation

# Export using the standalone file
PORTAPKG_BUNDLES_DIR=./bundles python3 portapkg.py export instrumation
```

!!! tip "No install required"
    The `portapkg.py` script is fully self-contained. You can use it both for
    **bundling** (on an online machine with pip) and **installing** (on an
    offline machine with pip). Just make sure `pip` is available on both ends.

## Environment variables

- `PORTAPKG_BUNDLES_DIR` — override the bundle directory (default: `./bundles/`)
