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
The set of files whose hotspot score exceeds a configurable threshold. Default: absolute score ≥ 50. Override with `--hotspot-threshold <value>` for a different absolute threshold, or `--hotspot-percentile <N>` to compute the threshold from the Nth percentile of global scores.
_Avoid_: Danger zone, critical files, problem areas

**Stack**:
The programming language of a repo's source files, auto-detected by lizard (e.g., js, java, python, typescript).
_Avoid_: Language, framework, tech stack

**Normalization score**:
A file's raw metric value rescaled to 0-100 globally across all repos in a run using IQR-aware min-max scaling. Outliers beyond IQR boundaries are capped before scaling. Scores are directly comparable across repos.
_Avoid_: Score, normalized value, score

**Config file**:
A YAML file (default: `repos.yaml`) that defines global include/exclude patterns and per-repo overrides. Each repo maps to an optional set of include and exclude globs that replace global defaults.
_Avoid_: Repo list, filter file, settings file

**Global defaults**:
The include/exclude patterns defined at the top level of the config file, applied to every repo unless a per-repo override exists.
_Avoid_: Defaults, base filters, common patterns

**Per-repo override**:
When a repo's include/exclude replaces global defaults entirely (not merged). If a repo has no override, it inherits global defaults.
_Avoid_: Repo filter, repo pattern, local exclude
