"""Tests for the distribution-validator helpers + an integration run."""

import validate_distribution as vd


def test_require_equal_flags_mismatch():
    errs = []
    vd.require_equal(errs, "label", "actual", "expected")
    assert len(errs) == 1


def test_require_equal_passes_on_match():
    errs = []
    vd.require_equal(errs, "label", "same", "same")
    assert errs == []


def test_require_subset_allows_extra_keys():
    errs = []
    vd.require_subset(
        errs,
        "s",
        {"source": "local", "path": "./p", "extra": 1},
        {"source": "local", "path": "./p"},
    )
    assert errs == []


def test_require_subset_flags_missing_key():
    errs = []
    vd.require_subset(errs, "s", {"source": "local"}, {"source": "local", "path": "./p"})
    assert len(errs) == 1


def test_require_subset_flags_wrong_value():
    errs = []
    vd.require_subset(
        errs, "s", {"source": "git", "path": "./p"}, {"source": "local", "path": "./p"}
    )
    assert len(errs) == 1


def test_require_subset_flags_non_dict():
    errs = []
    vd.require_subset(errs, "s", None, {"source": "local"})
    assert len(errs) == 1


def test_find_plugin_returns_single_match():
    errs = []
    catalog = {"plugins": [{"name": vd.PLUGIN_NAME, "source": "x"}]}
    found = vd.find_plugin(catalog, vd.ROOT, errs)
    assert found.get("name") == vd.PLUGIN_NAME
    assert errs == []


def test_find_plugin_flags_missing():
    errs = []
    vd.find_plugin({"plugins": []}, vd.ROOT, errs)
    assert len(errs) == 1


def test_semver_pattern():
    assert vd.SEMVER_PATTERN.fullmatch("0.1.0")
    assert vd.SEMVER_PATTERN.fullmatch("1.10.3")
    assert not vd.SEMVER_PATTERN.fullmatch("1.2")
    assert not vd.SEMVER_PATTERN.fullmatch("01.2.3")


def test_load_object_invalid_json(tmp_path, monkeypatch):
    monkeypatch.setattr(vd, "ROOT", tmp_path)
    bad = tmp_path / "bad.json"
    bad.write_text("{ not json", encoding="utf-8")
    errs = []
    assert vd.load_object(bad, errs) == {}
    assert len(errs) == 1


def test_load_object_rejects_non_object(tmp_path, monkeypatch):
    monkeypatch.setattr(vd, "ROOT", tmp_path)
    arr = tmp_path / "arr.json"
    arr.write_text("[1, 2, 3]", encoding="utf-8")
    errs = []
    assert vd.load_object(arr, errs) == {}
    assert any("must be a JSON object" in e for e in errs)


def test_real_repository_passes_distribution_validation():
    # Integration: the actual repo manifests + marketplaces must validate.
    assert vd.main([]) == 0


def test_main_accepts_matching_release_tag():
    assert vd.main(["--tag", "v0.1.0"]) == 0


def test_main_rejects_mismatched_release_tag(capsys):
    assert vd.main(["--tag", "v9.9.9"]) == 1
    assert "does not match manifest version" in capsys.readouterr().err


def test_main_flags_release_manifest_drift(tmp_path, monkeypatch, capsys):
    drifted = tmp_path / ".release-please-manifest.json"
    drifted.write_text('{".": "9.9.9"}', encoding="utf-8")
    monkeypatch.setattr(vd, "RELEASE_MANIFEST_PATH", drifted)
    assert vd.main([]) == 1
    assert "release-please-manifest.json" in capsys.readouterr().err
