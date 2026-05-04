"""Check for standard project structure (src layout or package directory)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


# Names that are never considered Python packages even if they contain __init__.py
_EXCLUDED_DIRS = {
    "tests",
    "test",
    "docs",
    "doc",
    "examples",
    "example",
    "scripts",
    "migrations",
    ".git",
    ".github",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "env",
    ".env",
    "dist",
    "build",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
}


@dataclass
class CheckResult:
    status: str  # "ok" | "warn" | "fail"
    message: str
    suggestions: list[str] = field(default_factory=list)


def _has_src_layout(path: str) -> bool:
    return os.path.isdir(os.path.join(path, "src"))


def _find_package_dirs(path: str) -> list[str]:
    """Return names of top-level directories that look like Python packages."""
    packages = []
    try:
        entries = os.listdir(path)
    except OSError:
        return packages

    for entry in entries:
        if entry in _EXCLUDED_DIRS or entry.startswith("."):
            continue
        full = os.path.join(path, entry)
        if os.path.isdir(full) and os.path.isfile(os.path.join(full, "__init__.py")):
            packages.append(entry)

    return packages


def check(path: str) -> CheckResult:
    if _has_src_layout(path):
        return CheckResult(status="ok", message="Standard src/ layout detected")

    packages = _find_package_dirs(path)
    if packages:
        names = ", ".join(packages)
        return CheckResult(status="ok", message=f"Package directory detected: {names}")

    return CheckResult(
        status="warn",
        message="Non-standard project structure (no src/ or package directory found)",
        suggestions=[
            "Consider using a src/ layout or placing your code in a proper Python package (directory with __init__.py).",
            "See: https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/",
        ],
    )
