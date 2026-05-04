"""Configuration parsing from pyproject.toml."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


@dataclass
class Config:
    ignore: list[str] = field(default_factory=list)
    strict: bool = False
    format: str = "rich"


def load_config(path: str) -> Config:
    """Load project-doctor configuration from pyproject.toml."""
    pyproject_path = os.path.join(path, "pyproject.toml")
    
    if not os.path.isfile(pyproject_path):
        return Config()

    try:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
    except Exception:
        return Config()

    tool_config = data.get("tool", {}).get("project-doctor", {})
    if not tool_config:
        return Config()

    ignore = tool_config.get("ignore", [])
    if isinstance(ignore, str):
        ignore = [ignore]
    
    strict = tool_config.get("strict", False)
    format_opt = tool_config.get("format", "rich")

    return Config(
        ignore=list(ignore),
        strict=bool(strict),
        format=str(format_opt),
    )
