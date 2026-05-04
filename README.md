<<<<<<< HEAD
# project-doctor
=======
# project-doctor 🩺

A command-line tool that scans a project directory and reports common repository hygiene issues — instantly.

---

## Features

| Check | What it looks for |
|---|---|
| **README** | Presence of `README.md` with `Installation` and `Usage` sections |
| **.gitignore** | Presence of `.gitignore` |
| **License** | Presence of `LICENSE` / `LICENSE.txt` |
| **Project Structure** | `src/` layout or a Python package directory |
| **Tests** | `tests/` or `test/` directory |
| **CI / CD** | GitHub Actions, GitLab CI, CircleCI, Travis CI, and more |

Each check reports one of:

- ✔ green — all good
- ⚠ yellow — present but incomplete
- ✖ red — missing, with actionable suggestions

A summary score (e.g. `4/6`) is printed at the end.

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

Scan a specific path:

```bash
project-doctor scan /path/to/my-project
```

You can also run it as a module:

```bash
python -m project_doctor.main scan /path/to/my-project
```

### Example output

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

───────────────────────────────────────────────────────────────────
Score  4/6  (4 passed  1 warnings  1 failed)
```

---

## Development

```bash
pip install -e ".[dev]"
pytest tests/
```

---

## License

MIT
>>>>>>> 9ab1561 (project doctors first committed version)
