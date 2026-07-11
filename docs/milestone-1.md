# Milestone 1: Project Setup & Foundation

## Objective
Set up the complete development environment, initialize version control, and establish the professional folder/file foundation for the Student Success Intelligence Platform — before writing any application code.

---

## Part A: Tools Installed & Why

### 1. Python 3
**What it is**: The programming language the entire project is built in.
**Why installed**: Without Python installed, none of our code can run. VS Code is just a text editor — it needs Python installed separately to execute `.py` files.
**Verification**: `python --version`

### 2. VS Code (Visual Studio Code)
**What it is**: The code editor (IDE) used to write, organize, and run the project.
**Extensions added**:
- **Python** (Microsoft) — syntax highlighting, running, and debugging Python files
- **Pylance** — smarter auto-complete and error-checking
- **SQLite Viewer** — visually browse database tables later

### 3. Git
**What it is**: Version control software that tracks every change made to the code over time.
**Why installed**: Lets us save "checkpoints" (commits), roll back if something breaks, and push code to GitHub.
**Verification**: `git --version`

### 4. GitHub Account
**What it is**: A website hosting Git repositories online — this project's public home and portfolio piece.

---

## Part B: Core Project Files

### File 1: `.gitignore`
**Purpose**: Tells Git which files/folders to never track or upload.

```
# Byte-compiled Python files
__pycache__/
*.pyc

# Virtual environment folder
venv/

# Database files (we don't upload real student data to GitHub)
data/*.db

# VS Code settings folder
.vscode/

# OS-generated files
.DS_Store
Thumbs.db
```

| Rule | Why |
|---|---|
| `__pycache__/`, `*.pyc` | Auto-generated compiled files, regenerate every run, not source code |
| `venv/` | Isolated Python environment; huge, fully reproducible via `requirements.txt` |
| `data/*.db` | Never commit real/sensitive database files |
| `.vscode/` | Machine-specific editor settings |
| `.DS_Store`, `Thumbs.db` | OS clutter (Mac/Windows), irrelevant to code |

### File 2: `requirements.txt`
**Purpose**: Lists every external Python library the project depends on.

```
pandas
numpy
matplotlib
```

- **pandas** — structured/tabular data handling (student marks, tables)
- **numpy** — fast numerical operations (mean, std dev, correlation)
- **matplotlib** — charts and graphs for visualizing performance

Anyone can install all three in one command:
```
pip install -r requirements.txt
```

### File 3: `README.md`
**Purpose**: The project's front door on GitHub — first thing visitors and recruiters see.

**Sections included**: Overview, Problem Statement, Features (checklist), Technology Stack, Folder Structure, Screenshots, Future Improvements, Status.

**Markdown syntax used**:
- `#`, `##` → headings
- `-` → bullet points
- `- [ ]` → clickable checkboxes
- ` ``` ` → code blocks (monospace, unformatted text)

---

## Part C: Python Virtual Environment

### `python -m venv venv`
Creates an isolated Python environment folder (`venv`) with its own private library storage, separate from the system-wide Python installation. Prevents version conflicts between projects and keeps the global Python installation clean.

### `venv\Scripts\Activate` (via `Set-ExecutionPolicy` on Windows)
"Switches on" the environment for the terminal session — confirmed by the prompt changing to:
```
(venv) PS C:\Users\...\Student-Success-Intelligence-Platform>
```
Windows PowerShell blocks scripts by default; `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` temporarily allows this for the current session only.

### `pip install -r requirements.txt`
Installs pandas, numpy, matplotlib (and sub-dependencies like pillow, cycler, fonttools) into the isolated `venv`. Confirmed by:
```
Successfully installed contourpy-1.3.3 cycler-0.12.1 fonttools-4.63.0 kiwisolver-1.5.0
matplotlib-3.11.0 numpy-2.5.1 packaging-26.2 pandas-3.0.3 pillow-12.3.0 pyparsing-3.3.2
python-dateutil-2.9.0.post0 six-1.17.0 tzdata-2026.3
```

---

## Part D: Git Version Control

| Command | Purpose |
|---|---|
| `git init` | Turns the folder into a Git repository (creates hidden `.git/`) |
| `git status` | Shows tracked/untracked/staged file state |
| `git add .` | Stages all non-ignored files for the next commit |
| `git config --global user.email "..."` / `user.name "..."` | Sets committer identity (required by Git) |
| `git commit -m "..."` | Permanently saves staged files as a labeled checkpoint |
| `git commit --amend --reset-author --no-edit` | Fixes author info on the most recent commit without changing its content |
| `git remote add origin <url>` | Links the local repo to the GitHub repo, nicknamed `origin` |
| `git remote -v` | Verifies the fetch/push URLs are correctly linked |
| `git branch -M main` | Renames the default branch from `master` to `main` |
| `git push -u origin main` | Uploads commits to GitHub; `-u` sets `origin main` as the default push target |

---

## Part E: Verification

- Repository confirmed live at: `https://github.com/rushikapatel-016/Student-Success-Intelligence-Platform-`
- First commit visible: `"Initial project setup with README, gitignore, and requirements"`
- All 3 files (`.gitignore`, `README.md`, `requirements.txt`) present and correctly rendered
- Repository visibility: **Public**

---

## Milestone 1 Status: ✅ Complete

**Skills practiced**: environment setup, dependency isolation, Git fundamentals, GitHub authentication, professional documentation writing, debugging (PowerShell execution policy, Git author identity, Markdown formatting).