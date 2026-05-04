"""Check for containerization files."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class CheckResult:
    status: str
    message: str
    suggestions: list[str] = field(default_factory=list)


def check(path: str) -> CheckResult:
    files = [f.lower() for f in os.listdir(path)] if os.path.isdir(path) else []
    
    container_files = [
        "dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        "containerfile",
    ]
    
    found = [f for f in container_files if f in files]
    
    if found:
        return CheckResult(status="ok", message="Container configuration found")
        
    return CheckResult(
        status="warn",
        message="No container configuration found",
        suggestions=[
            "If this is a deployable service, consider adding a Dockerfile."
        ],
    )
