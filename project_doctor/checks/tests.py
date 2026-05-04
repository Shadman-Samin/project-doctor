"""Check for tests directory presence."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


TEST_DIR_NAMES = ["tests", "test"]


@dataclass
class CheckResult:
    status: str  # "ok" | "warn" | "fail"
    message: str
    suggestions: list[str] = field(default_factory=list)


def check(path: str) -> CheckResult:
    for name in TEST_DIR_NAMES:
        if os.path.isdir(os.path.join(path, name)):
            return CheckResult(status="ok", message=f"Tests directory found ({name}/)")

    return CheckResult(
        status="fail",
        message="No tests directory found",
        suggestions=[
            "Create a tests/ directory and add unit tests for your project.",
            "Consider using pytest: https://docs.pytest.org",
        ],
    )


def fix(path: str) -> None:
    tests_path = os.path.join(path, "tests")
    if not os.path.isdir(tests_path):
        os.makedirs(tests_path, exist_ok=True)
        init_file = os.path.join(tests_path, "__init__.py")
        with open(init_file, "w", encoding="utf-8") as f:
            f.write("")
