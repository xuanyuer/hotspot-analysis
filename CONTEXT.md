# Code Hotspot Analysis

Analyzes git repositories to identify code hotspots — files that are both high-churn and high-complexity — using git history and static analysis.

## Language

**Repo**:
A git repository to be analyzed. Contains source files tracked by git on its main branch.
_Avoid_: Project, codebase, service

**File**:
A tracked source code file within a repo, subject to include/exclude glob filters.
_Avoid_: Module, unit, asset

**Churn**:
A file-level metric derived from git history — number of commits touching the file, total lines added and removed, and distinct authors. Higher = more frequently changed.
_Avoid_: Activity, change frequency, volatility

**Complexity**:
A file-level metric derived from static analysis — weighted combination of function-level cyclomatic complexity, average complexity, and file length. Higher = more structurally complex.
_Avoid_: Cyclomatic complexity, technical debt, danger

**Hotspot score**:
A 0-100 intensity measure computed as the geometric mean of normalized churn and normalized complexity: √(churn × complexity).
_Avoid_: Risk score, hotspot index, combined score

**Hotspot zone**:
The set of files whose hotspot score exceeds a configurable percentile threshold (default: 75th percentile within the repo). These are the files flagged for review.
_Avoid_: Danger zone, critical files, problem areas

**Stack**:
The programming language of a repo's source files, auto-detected by lizard (e.g., js, java, python, typescript).
_Avoid_: Language, framework, tech stack

**Normalization score**:
A file's raw metric value rescaled to 0-100 within a repo using IQR-aware min-max scaling. Outliers beyond IQR boundaries are capped before scaling.
_Avoid_: Score, normalized value, score
