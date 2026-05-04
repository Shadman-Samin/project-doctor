# project-doctor 🩺

A command-line tool that scans a project directory and reports common repository hygiene issues — instantly. It helps ensure that your projects adhere to best practices for maintainability, collaboration, and deployment.

---

## Features

Project Doctor performs a variety of checks on your codebase:

| Check | What it looks for |
|---|---|
| **README** | Presence of `README.md` with `Installation` and `Usage` sections |
| **.gitignore** | Presence of `.gitignore` |
| **License** | Presence of `LICENSE` / `LICENSE.txt` |
| **Project Structure** | `src/` layout or a Python package directory |
| **Tests** | `tests/` or `test/` directory |
| **CI / CD** | GitHub Actions, GitLab CI, CircleCI, Travis CI, and more |
| **Contributing** | Presence of `CONTRIBUTING.md` or similar guidelines |
| **Formatting** | Pre-commit hooks, Black, Flake8, or other formatting configs |
| **Dependencies** | `requirements.txt`, `pyproject.toml`, or other dependency files |
| **Documentation** | `docs/` or `wiki/` directory |
| **EditorConfig** | Presence of `.editorconfig` |
| **Containerization**| `Dockerfile` or `docker-compose.yml` |

Each check reports one of:

- ✔ green — all good
- ⚠ yellow — present but incomplete
- ✖ red — missing, with actionable suggestions

A summary score (e.g. `10/12`) is printed at the end.

### Additional Capabilities

- **Remote Scanning**: Scan public GitHub repositories directly via URL.
- **Auto-Fix**: Automatically fix simple missing files like `.gitignore` or `.editorconfig` using the `--fix` flag.
- **Strict Mode**: Perfect for CI/CD environments, exiting with code `1` if any check fails.
- **JSON Output**: Output results in JSON format for parsing and integrations.
- **Ignore Checks**: Skip specific checks you don't need.

---

## Installation

```bash
pip install project-doctor
```

Or install from source:

```bash
git clone https://github.com/yourname/project-doctor.git
cd project-doctor
pip install -e .
```

---

## Usage

Scan the current directory:

```bash
project-doctor scan
```

Scan a specific local path:

```bash
project-doctor scan /path/to/my-project
```

Scan a remote repository:

```bash
project-doctor scan https://github.com/user/repo
```

### CLI Options

- `--strict`: Exit with code 1 if any check fails (useful for CI/CD).
- `--format [rich|json]`: Specify the output format.
- `--fix`: Attempt to auto-fix simple missing files.
- `--ignore <check_name>`: Ignore a specific check. Can be used multiple times.

**Example with options:**

```bash
project-doctor scan . --strict --format json --fix
```

### Example Output (Rich)

```
────────────── project-doctor  /home/user/my-project ──────────────

README               ✔  README looks good
.gitignore           ✔  .gitignore found
License              ✖  LICENSE missing
                        → Add a LICENSE file so users know the terms.
                        → Choose one at: https://choosealicense.com
Project Structure    ✔  Package directory detected: my_project
Tests                ⚠  No tests directory found
                        → Create a tests/ directory and add unit tests.
CI / CD              ✔  CI configuration found (GitHub Actions)
Contributing         ✔  CONTRIBUTING.md found
Dependencies         ✔  Dependencies found
...

───────────────────────────────────────────────────────────────────
Score  10/12  (10 passed  1 warnings  1 failed)
```

---

## Configuration

You can configure `project-doctor` by creating a configuration file in your project directory. 
By default, `project-doctor` will look for a `project-doctor.toml` or `pyproject.toml` with a `[tool.project-doctor]` section to read settings like strict mode, format, and ignored checks.

---

## Development

```bash
pip install -e ".[dev]"
pytest tests/
```

---

## License

MIT
