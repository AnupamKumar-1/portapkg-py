import json
import os

from portapkg.bundler.manifest import build_manifest, read_manifest, write_manifest


class TestBuildManifest:
    def test_build_manifest_structure(self):
        deps = [{"name": "pkg", "version": "1.0"}]
        result = build_manifest("testpkg", "2.0", deps, "linux_x86_64", "312")
        assert result["name"] == "testpkg"
        assert result["version"] == "2.0"
        assert result["source_platform"] == "linux_x86_64"
        assert result["source_python"] == "312"
        assert "date_bundled" in result
        assert result["dependencies"] == deps

    def test_build_manifest_empty_deps(self):
        result = build_manifest("testpkg", "1.0", [], "win_amd64", "311")
        assert result["dependencies"] == []


class TestWriteManifest:
    def test_write_manifest_creates_file(self, tmp_bundle_dir):
        data = {"name": "test", "version": "1.0"}
        path = write_manifest(tmp_bundle_dir, data)
        assert os.path.exists(path)
        assert path == os.path.join(tmp_bundle_dir, "manifest.json")

    def test_write_manifest_content(self, tmp_bundle_dir):
        data = {"name": "test", "version": "1.0", "deps": []}
        write_manifest(tmp_bundle_dir, data)
        with open(os.path.join(tmp_bundle_dir, "manifest.json")) as f:
            loaded = json.load(f)
        assert loaded == data


class TestReadManifest:
    def test_read_manifest_exists(self, tmp_bundle_dir, sample_manifest_data):
        path = os.path.join(tmp_bundle_dir, "manifest.json")
        with open(path, "w") as f:
            json.dump(sample_manifest_data, f)
        result = read_manifest(tmp_bundle_dir)
        assert result == sample_manifest_data

    def test_read_manifest_not_found(self, tmp_bundle_dir):
        result = read_manifest(tmp_bundle_dir)
        assert result is None

    def test_read_manifest_empty_dir(self, tmp_bundle_dir):
        result = read_manifest(tmp_bundle_dir)
        assert result is None
