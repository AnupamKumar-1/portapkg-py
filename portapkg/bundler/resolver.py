import os
import re
import subprocess
import sys
import tempfile


def _parse_package_version(filename):
    if filename.endswith(".whl"):
        stem = filename[:-4]
        parts = stem.split("-")
        if len(parts) < 4:
            return None, None
        if "." in parts[-4]:
            name = "-".join(parts[:-4])
            version = parts[-4]
        else:
            name = "-".join(parts[:-5])
            version = parts[-5]
        return name, version
    elif filename.endswith((".tar.gz", ".zip", ".tar.bz2")):
        for suffix in (".tar.gz", ".tar.bz2", ".zip"):
            if filename.endswith(suffix):
                stem = filename[: -len(suffix)]
                break
        parts = stem.split("-")
        if len(parts) >= 2 and re.match(r"^\d", parts[-1]):
            return "-".join(parts[:-1]), parts[-1]
        if len(parts) >= 2:
            return parts[0], parts[1]
    return None, None


def resolve_dependencies(package):
    with tempfile.TemporaryDirectory(prefix="portapkg-resolve-") as tmpdir:
        cmd = [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--dest",
            tmpdir,
            package,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to resolve dependencies for {package}:\n{result.stderr}"
            )

        deps = {}
        for fname in os.listdir(tmpdir):
            pkg_name, version = _parse_package_version(fname)
            if pkg_name and version:
                pkg_name = pkg_name.lower().replace("_", "-")
                if pkg_name not in deps:
                    deps[pkg_name] = version

    return deps


def freeze_snapshot():
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pip freeze failed:\n{result.stderr}")

    packages = {}
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-e") or " @ " in line:
            continue
        if "==" in line:
            name, version = line.split("==", 1)
            packages[name.lower().replace("_", "-")] = version
    return packages
