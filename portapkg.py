#!/usr/bin/env python3
"""
portapkg.py - Portable offline Python package installer.

Self-contained single file (stdlib + subprocess only).
Copy this file + bundles/ folder to an offline machine and run:
    python portapkg.py install <package>
    python portapkg.py list
"""

import argparse
import json
import os
import platform as _platform
import subprocess
import sys


BUNDLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bundles")


def _read_manifest(bundle_dir):
    path = os.path.join(bundle_dir, "manifest.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def _detect_platform():
    system = sys.platform
    machine = _platform.machine().lower()
    if system == "win32":
        return "win_amd64" if machine in ("amd64", "x86_64") else "win32"
    elif system == "linux":
        return "linux_aarch64" if machine in ("aarch64", "arm64") else "linux_x86_64"
    elif system == "darwin":
        return "macosx_13_0_arm64" if machine in ("arm64", "aarch64") else "macosx_13_0_x86_64"
    return f"{system}_{machine}"


def _detect_python():
    return f"{sys.version_info.major}{sys.version_info.minor}"


def _parse_wheel(filename):
    if not filename.endswith(".whl"):
        return None
    parts = filename[:-4].split("-")
    if len(parts) < 5:
        return None
    return {"python_tag": parts[-3], "abi_tag": parts[-2], "platform_tag": parts[-1]}


def _py_tag_matches(tag, cur_ver):
    for t in tag.split("."):
        t = t.strip()
        if t == "*":
            return True
        v = t[2:] if t.startswith("cp") or t.startswith("py") else t
        if not v:
            return True
        major = sys.version_info.major
        minor = sys.version_info.minor
        if int(v[0]) != major:
            continue
        if len(v) < 2:
            return True
        if int(v[1:]) == minor:
            return True
    return False


def _plat_matches(wheel_plat, cur_plat):
    if wheel_plat == "any":
        return True
    a = wheel_plat.replace("-", "_").replace(".", "_").lower()
    b = cur_plat.replace("-", "_").replace(".", "_").lower()
    if a == b:
        return True
    if (a.startswith("linux") or a.startswith("manylinux")) and (
        b.startswith("linux") or b.startswith("manylinux")
    ):
        a_arch = a.split("_")[-1]
        b_arch = b.split("_")[-1]
        if a_arch == b_arch:
            return True
    if a.startswith("macosx") and b.startswith("macosx"):
        return True
    if a.startswith("win") and b.startswith("win"):
        a_arch = a.split("_")[-1] if "_" in a else a
        b_arch = b.split("_")[-1] if "_" in b else b
        if a_arch == b_arch:
            return True
    return False


def _check_pip():
    r = subprocess.run(
        [sys.executable, "-m", "pip", "--version"], capture_output=True, text=True
    )
    return r.returncode == 0


def cmd_install(args):
    if not _check_pip():
        print("ERROR: pip is not available. Cannot install.", file=sys.stderr)
        sys.exit(1)

    bundle_dir = os.path.join(BUNDLES_DIR, args.package)
    if not os.path.isdir(bundle_dir):
        print(
            f"ERROR: Bundle for '{args.package}' not found in {BUNDLES_DIR}.\n"
            f"Copy the bundle directory to this machine first.",
            file=sys.stderr,
        )
        sys.exit(1)

    manifest = _read_manifest(bundle_dir)
    if manifest is None:
        print(f"ERROR: No manifest in {bundle_dir}", file=sys.stderr)
        sys.exit(1)

    cur_plat = _detect_platform()
    cur_py = _detect_python()
    wheels_dir = os.path.join(bundle_dir, "wheels")

    if not os.path.isdir(wheels_dir):
        print(f"ERROR: No wheels directory in {bundle_dir}", file=sys.stderr)
        sys.exit(1)

    compatible = []
    for fname in os.listdir(wheels_dir):
        parsed = _parse_wheel(fname)
        if parsed is None:
            continue
        if not _py_tag_matches(parsed["python_tag"], cur_py):
            continue
        if not _plat_matches(parsed["platform_tag"], cur_plat):
            continue
        compatible.append(fname)

    if not compatible:
        dep_info = []
        for d in manifest.get("dependencies") or []:
            dep_info.append(f"{d.get('name', '?')}=={d.get('version', '?')}")
        print(
            f"ERROR: No compatible wheel found for {args.package}\n"
            f"  Current platform: {cur_plat}\n"
            f"  Current Python:   {cur_py}\n"
            f"  Bundled deps:     {', '.join(dep_info) if dep_info else 'none'}\n"
            f"Try bundling with --snapshot on this machine.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Installing {args.package} from bundle...")
    print(f"  Platform: {cur_plat}")
    print(f"  Python:   {cur_py}")
    print(f"  Wheels:   {len(compatible)} compatible found")

    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--no-index",
        "--find-links",
        wheels_dir,
        args.package,
    ]
    if args.target:
        cmd.extend(["--target", args.target])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: Installation failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    print(result.stdout)
    print(f"Successfully installed {args.package}")


def cmd_list(args):
    if not os.path.isdir(BUNDLES_DIR):
        print("No bundles directory found.")
        return
    bundles = sorted(
        d
        for d in os.listdir(BUNDLES_DIR)
        if os.path.isdir(os.path.join(BUNDLES_DIR, d))
    )
    if not bundles:
        print("No bundles available.")
        return
    print("Available bundles:")
    for name in bundles:
        m = _read_manifest(os.path.join(BUNDLES_DIR, name))
        if m:
            print(
                f"  {name}  v{m.get('version', '?')}  ({m.get('date_bundled', '?')})"
            )
        else:
            print(f"  {name}  (no manifest)")


def main():
    parser = argparse.ArgumentParser(
        prog="portapkg.py",
        description="Portable offline Python package installer",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_install = sub.add_parser("install", help="Install a bundled package")
    p_install.add_argument("package", help="Package name")
    p_install.add_argument(
        "--target", help="Custom install path (e.g. ./venv/Lib/site-packages)"
    )
    p_install.set_defaults(func=cmd_install)

    p_list = sub.add_parser("list", help="List available bundles")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
