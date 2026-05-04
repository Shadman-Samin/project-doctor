"""Unit tests for individual project-doctor checks."""

from __future__ import annotations

import os
import tempfile

import pytest

from project_doctor.checks import (
    ci, gitignore, license, readme, structure, tests as tests_check,
    contributing, formatting, dependencies, documentation, editorconfig, container
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_dir(*rel_paths: str, base: str) -> None:
    for rel in rel_paths:
        os.makedirs(os.path.join(base, rel), exist_ok=True)


def make_file(rel_path: str, base: str, content: str = "") -> None:
    full = os.path.join(base, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)


# ── README ────────────────────────────────────────────────────────────────────

class TestReadmeCheck:
    def test_missing(self, tmp_path):
        r = readme.check(str(tmp_path))
        assert r.status == "fail"

    def test_empty(self, tmp_path):
        make_file("README.md", base=str(tmp_path), content="# My Project\n")
        r = readme.check(str(tmp_path))
        assert r.status == "warn"
        assert "Installation" in r.message or "Usage" in r.message

    def test_has_all_sections(self, tmp_path):
        make_file(
            "README.md",
            base=str(tmp_path),
            content="# Project\n\n## Installation\n\n...\n\n## Usage\n\n...\n",
        )
        r = readme.check(str(tmp_path))
        assert r.status == "ok"

    def test_partial_sections(self, tmp_path):
        make_file("README.md", base=str(tmp_path), content="## Installation\n")
        r = readme.check(str(tmp_path))
        assert r.status == "warn"
        assert "Usage" in r.message


# ── .gitignore ────────────────────────────────────────────────────────────────

class TestGitignoreCheck:
    def test_missing(self, tmp_path):
        r = gitignore.check(str(tmp_path))
        assert r.status == "fail"

    def test_present(self, tmp_path):
        make_file(".gitignore", base=str(tmp_path), content="*.pyc\n")
        r = gitignore.check(str(tmp_path))
        assert r.status == "ok"


# ── License ───────────────────────────────────────────────────────────────────

class TestLicenseCheck:
    def test_missing(self, tmp_path):
        r = license.check(str(tmp_path))
        assert r.status == "fail"

    def test_license_file(self, tmp_path):
        make_file("LICENSE", base=str(tmp_path), content="MIT License\n")
        r = license.check(str(tmp_path))
        assert r.status == "ok"

    def test_license_txt(self, tmp_path):
        make_file("LICENSE.txt", base=str(tmp_path), content="MIT\n")
        r = license.check(str(tmp_path))
        assert r.status == "ok"


# ── Structure ─────────────────────────────────────────────────────────────────

class TestStructureCheck:
    def test_no_structure(self, tmp_path):
        r = structure.check(str(tmp_path))
        assert r.status == "warn"

    def test_src_layout(self, tmp_path):
        make_dir("src", base=str(tmp_path))
        r = structure.check(str(tmp_path))
        assert r.status == "ok"

    def test_package_dir(self, tmp_path):
        make_dir("mypackage", base=str(tmp_path))
        make_file("mypackage/__init__.py", base=str(tmp_path))
        r = structure.check(str(tmp_path))
        assert r.status == "ok"

    def test_tests_dir_not_counted(self, tmp_path):
        make_dir("tests", base=str(tmp_path))
        make_file("tests/__init__.py", base=str(tmp_path))
        r = structure.check(str(tmp_path))
        assert r.status == "warn"


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestTestsCheck:
    def test_missing(self, tmp_path):
        r = tests_check.check(str(tmp_path))
        assert r.status == "fail"

    def test_tests_dir(self, tmp_path):
        make_dir("tests", base=str(tmp_path))
        r = tests_check.check(str(tmp_path))
        assert r.status == "ok"

    def test_test_dir(self, tmp_path):
        make_dir("test", base=str(tmp_path))
        r = tests_check.check(str(tmp_path))
        assert r.status == "ok"


# ── CI ────────────────────────────────────────────────────────────────────────

class TestCICheck:
    def test_missing(self, tmp_path):
        r = ci.check(str(tmp_path))
        assert r.status == "fail"

    def test_github_actions(self, tmp_path):
        make_dir(".github/workflows", base=str(tmp_path))
        r = ci.check(str(tmp_path))
        assert r.status == "ok"

    def test_travis(self, tmp_path):
        make_file(".travis.yml", base=str(tmp_path), content="language: python\n")
        r = ci.check(str(tmp_path))
        assert r.status == "ok"

    def test_circleci(self, tmp_path):
        make_dir(".circleci", base=str(tmp_path))
        r = ci.check(str(tmp_path))
        assert r.status == "ok"


# ── Contributing ──────────────────────────────────────────────────────────────

class TestContributingCheck:
    def test_missing(self, tmp_path):
        r = contributing.check(str(tmp_path))
        assert r.status == "warn"

    def test_present(self, tmp_path):
        make_file("CONTRIBUTING.md", base=str(tmp_path))
        make_file("CODE_OF_CONDUCT.md", base=str(tmp_path))
        make_file(".github/ISSUE_TEMPLATE/bug.md", base=str(tmp_path))
        r = contributing.check(str(tmp_path))
        assert r.status == "ok"


# ── Formatting ────────────────────────────────────────────────────────────────

class TestFormattingCheck:
    def test_missing(self, tmp_path):
        r = formatting.check(str(tmp_path))
        assert r.status == "warn"

    def test_present(self, tmp_path):
        make_file(".pre-commit-config.yaml", base=str(tmp_path))
        r = formatting.check(str(tmp_path))
        assert r.status == "ok"


# ── Dependencies ──────────────────────────────────────────────────────────────

class TestDependenciesCheck:
    def test_missing(self, tmp_path):
        r = dependencies.check(str(tmp_path))
        assert r.status == "fail"

    def test_present(self, tmp_path):
        make_file("requirements.txt", base=str(tmp_path))
        r = dependencies.check(str(tmp_path))
        assert r.status == "ok"


# ── Documentation ─────────────────────────────────────────────────────────────

class TestDocumentationCheck:
    def test_missing(self, tmp_path):
        r = documentation.check(str(tmp_path))
        assert r.status == "warn"

    def test_present(self, tmp_path):
        make_dir("docs", base=str(tmp_path))
        r = documentation.check(str(tmp_path))
        assert r.status == "ok"


# ── EditorConfig ──────────────────────────────────────────────────────────────

class TestEditorConfigCheck:
    def test_missing(self, tmp_path):
        r = editorconfig.check(str(tmp_path))
        assert r.status == "warn"

    def test_present(self, tmp_path):
        make_file(".editorconfig", base=str(tmp_path))
        r = editorconfig.check(str(tmp_path))
        assert r.status == "ok"


# ── Container ─────────────────────────────────────────────────────────────────

class TestContainerCheck:
    def test_missing(self, tmp_path):
        r = container.check(str(tmp_path))
        assert r.status == "warn"

    def test_present(self, tmp_path):
        make_file("Dockerfile", base=str(tmp_path))
        r = container.check(str(tmp_path))
        assert r.status == "ok"
