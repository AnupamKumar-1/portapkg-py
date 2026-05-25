import os
import subprocess
import sys

from portapkg.installer.platform import DEFAULT_PLATFORMS, DEFAULT_PYTHON_VERSIONS


def download_wheels(
    package,
    version,
    dest_dir,
    platforms=None,
    python_versions=None,
    no_binary_fallback=True,
):
    if platforms is None:
        platforms = DEFAULT_PLATFORMS
    if python_versions is None:
        python_versions = DEFAULT_PYTHON_VERSIONS

    failures = []
    successes = []
    spec = f"{package}=={version}"

    for plat in platforms:
        for pyver in python_versions:
            pyver_dotted = f"{pyver[0]}.{pyver[1:]}"
            cmd = [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--dest",
                dest_dir,
                "--platform",
                plat,
                "--python-version",
                pyver_dotted,
                "--only-binary=:all:",
                "--no-deps",
                spec,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                successes.append((plat, pyver, "binary"))
            else:
                if no_binary_fallback:
                    cmd_fallback = [
                        sys.executable,
                        "-m",
                        "pip",
                        "download",
                        "--dest",
                        dest_dir,
                        "--platform",
                        plat,
                        "--python-version",
                        pyver_dotted,
                        "--no-deps",
                        spec,
                    ]
                    result2 = subprocess.run(
                        cmd_fallback, capture_output=True, text=True
                    )
                    if result2.returncode == 0:
                        successes.append((plat, pyver, "source"))
                        _warn(
                            f"{package}=={version}: no binary wheel for "
                            f"{plat}/{pyver}, using source dist"
                        )
                    else:
                        failures.append((plat, pyver, result2.stderr))
                        _warn(
                            f"{package}=={version}: no wheel available for "
                            f"{plat}/{pyver}"
                        )
                else:
                    failures.append((plat, pyver, result.stderr))

    return successes, failures


def download_single_platform(package, version, dest_dir):
    spec = f"{package}=={version}"
    cmd = [
        sys.executable,
        "-m",
        "pip",
        "download",
        "--dest",
        dest_dir,
        "--no-deps",
        spec,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to download {spec}:\n{result.stderr}"
        )
    return True


def _warn(msg):
    print(f"WARNING: {msg}", file=sys.stderr)
