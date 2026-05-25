import json
import os
import tempfile

import pytest


@pytest.fixture
def tmp_bundle_dir():
    with tempfile.TemporaryDirectory(prefix="portapkg-test-") as tmpdir:
        bundle = os.path.join(tmpdir, "testpkg")
        os.makedirs(os.path.join(bundle, "wheels"))
        yield bundle


@pytest.fixture
def sample_manifest_data():
    return {
        "name": "testpkg",
        "version": "1.0.0",
        "date_bundled": "2026-05-25T12:00:00",
        "source_platform": "macosx_13_0_arm64",
        "source_python": "312",
        "dependencies": [
            {"name": "testpkg", "version": "1.0.0"},
            {"name": "dep1", "version": "2.0.0"},
        ],
    }


@pytest.fixture
def manifest_with_wheels(tmp_bundle_dir, sample_manifest_data):
    manifest_path = os.path.join(tmp_bundle_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(sample_manifest_data, f, indent=2)
    wheels_dir = os.path.join(tmp_bundle_dir, "wheels")
    wheel_files = [
        "testpkg-1.0.0-py3-none-any.whl",
        "dep1-2.0.0-py3-none-any.whl",
        "numpy-1.26.0-cp312-cp312-manylinux2014_x86_64.whl",
        "numpy-1.26.0-cp312-cp312-win_amd64.whl",
    ]
    for wf in wheel_files:
        path = os.path.join(wheels_dir, wf)
        with open(path, "w") as f:
            f.write("")
    return tmp_bundle_dir, sample_manifest_data, wheel_files
