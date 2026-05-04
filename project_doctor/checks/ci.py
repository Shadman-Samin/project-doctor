"""Check for CI configuration presence."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


CI_PATHS = [
    (".github/workflows", "GitHub Actions"),
    (".gitlab-ci.yml", "GitLab CI"),
    (".circleci", "CircleCI"),
    ("Jenkinsfile", "Jenkins"),
    (".travis.yml", "Travis CI"),
    ("azure-pipelines.yml", "Azure Pipelines"),
    (".buildkite", "Buildkite"),
]


@dataclass
class CheckResult:
    status: str  # "ok" | "warn" | "fail"
    message: str
    suggestions: list[str] = field(default_factory=list)


def check(path: str) -> CheckResult:
    for rel_path, label in CI_PATHS:
        full = os.path.join(path, rel_path)
        if os.path.exists(full):
            return CheckResult(status="ok", message=f"CI configuration found ({label})")

    return CheckResult(
        status="fail",
        message="No CI configuration found",
        suggestions=[
            "Add a CI pipeline to automate testing on every push.",
            "GitHub Actions is a great starting point: https://docs.github.com/en/actions",
        ],
    )
