"""CLI entry point for project-doctor."""

from __future__ import annotations

import sys
import tempfile
import subprocess
from pathlib import Path

import typer
from rich.console import Console

from project_doctor.scanner import scan
from project_doctor.config import load_config
from typing import Optional

app = typer.Typer(
    name="project-doctor",
    help="Scan a project directory for common repository hygiene issues.",
    add_completion=False,
)

console = Console(stderr=True)


@app.command()
def scan_cmd(
    path: str = typer.Argument(
        ".",
        help="Path to the project directory to scan. Defaults to current directory.",
        show_default=True,
    ),
    strict: Optional[bool] = typer.Option(
        None,
        "--strict",
        help="Exit with code 1 if any check fails.",
    ),
    format_opt: Optional[str] = typer.Option(
        None,
        "--format",
        help="Output format (rich or json).",
    ),
    fix: bool = typer.Option(
        False,
        "--fix",
        help="Attempt to auto-fix missing basic files like .gitignore.",
    ),
    ignore: Optional[list[str]] = typer.Option(
        None,
        "--ignore",
        help="List of checks to ignore.",
    ),
) -> None:
    """Scan a project directory and report hygiene issues."""
    is_remote = path.startswith("http://") or path.startswith("https://")

    if is_remote:
        if fix:
            console.print("[yellow]Warning:[/yellow] The --fix flag is disabled when scanning remote repositories.")
            fix = False
            
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                subprocess.run(
                    ["git", "clone", "--depth", "1", path, tmpdir],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                console.print(f"[red]Error:[/red] Failed to clone repository: {path}")
                console.print(f"[dim]{e.stderr.decode('utf-8', errors='ignore')}[/dim]")
                raise typer.Exit(code=1)
                
            config = load_config(tmpdir)
            final_strict = strict if strict is not None else config.strict
            final_format = format_opt if format_opt is not None else config.format
            final_ignore = ignore if ignore else config.ignore

            scan(
                tmpdir,
                strict=final_strict,
                output_format=final_format,
                fix=fix,
                ignore=final_ignore,
                display_name=path,
            )
        return

    target = Path(path)

    if not target.exists():
        console.print(f"[red]Error:[/red] Path does not exist: {path}")
        raise typer.Exit(code=1)

    if not target.is_dir():
        console.print(f"[red]Error:[/red] Path is not a directory: {path}")
        raise typer.Exit(code=1)

    config = load_config(str(target))
    
    final_strict = strict if strict is not None else config.strict
    final_format = format_opt if format_opt is not None else config.format
    final_ignore = ignore if ignore else config.ignore

    scan(
        str(target),
        strict=final_strict,
        output_format=final_format,
        fix=fix,
        ignore=final_ignore,
    )

# Allow: python -m project_doctor.main scan .
app.command(name="scan")(scan_cmd)

if __name__ == "__main__":
    app()
