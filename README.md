# Code Hotspot Analysis Tool

Analyzes git repositories to identify **code hotspots** — files that are both high-churn and high-complexity — using git history and static analysis.

## What is a Code Hotspot?

A code hotspot is a file that changes frequently (high churn) and has complex structure (high complexity). The combination signals files that are likely candidates for refactoring, re-assignment, or increased code review attention.

The hotspot score is computed as:

```
hotspot_score = √(normalized_churn × normalized_complexity) × 100
```

- **Churn**: derived from `git log --numstat` (commit count, lines added/removed, distinct authors)
- **Complexity**: derived from [lizard](https://github.com/terrencey/lizard) cyclomatic analysis
- **Normalization**: IQR-aware min-max scaling within each repo (outliers capped at Q3 + 1.5×IQR)
- **Hotspot zone**: files scoring above the configurable percentile threshold (default: 75th)

## Installation

```bash
# Clone
git clone https://github.com/xuanyuer/hotspot-analysis.git
cd hotspot-analysis

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (3 core deps, no bloat)
pip install -r requirements.txt
```

**Dependencies:** `lizard`, `matplotlib`, `plotly` (pandas removed — not used)

## Quick Start

Analyze a single repository:

```bash
python main.py --repo /path/to/repo
```

Output is written to `./hotspot-output/<repo-name>/`:
- `ranked.csv` — ranked table with all scores
- `ranked.md` — Markdown formatted report
- `scatter.png` — static matplotlib scatter plot
- `report.html` — interactive plotly HTML with hover tooltips

### Multi-repo analysis

Create a repo-list file (one per line, `#` for comments, optional inline `include:`/`exclude:` per repo):

```
# My projects
/path/to/service-a include:*.java include:*.kt exclude:build/* exclude:gen/*
/path/to/service-b include:*.js include:*.ts
/path/to/legacy-service
# Falls back to global --include/--exclude if no per-repo patterns
```

Run batch analysis:

```bash
python main.py --repo-list repos.txt --output ./hotspot-output
```

Output structure:
```
hotspot-output/
├── service-a/
│   ├── ranked.csv
│   ├── ranked.md
│   ├── scatter.png
│   └── report.html
├── service-b/
│   ├── ...
├── combined/
│   ├── combined.csv          — all files from all repos, sorted by hotspot score
│   ├── combined.md           — per-repo summary + ranked table
│   └── consolidated.html     — management-facing single-file report
```

Failed repos are listed in the run summary and in `combined/combined.md`.

## CLI Reference

```
python main.py --help

usage: main.py [-h] [--repo REPO] [--repo-list REPO_LIST]
               [--include INCLUDE [INCLUDE ...]] [--exclude EXCLUDE [EXCLUDE ...]]
               [--since SINCE] [--output OUTPUT] [--hotspot-percentile HOTSPOT_PERCENTILE]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--repo` | Path to a git repository | (required if no --repo-list) |
| `--repo-list` | Path to file with repo paths (one per line) | |
| `--include` | Glob patterns to include (e.g., `--include *.java *.py`) | all tracked files |
| `--exclude` | Glob patterns to exclude (e.g., `--exclude test/*`) | language-specific defaults |
| `--since` | Time window for churn (e.g., `6months`, `2years`) | full history |

### Per-repo include/exclude (repo-list only)

In the repo-list file, append `include:` and `exclude:` tokens after the repo path.
Per-repo patterns **replace** (not merge with) global patterns for that repo:

```
/path/to/repo include:*.java exclude:build/*   # replaces global --include/--exclude
/path/to/other                                # falls back to global
```

- `include:*.java` — include only `.java` files for this repo
- `exclude:build/*` — additionally exclude `build/` for this repo
- No per-repo patterns → global `--include`/`--exclude` apply
- Per-repo `include:` without `--include` flag → no files included unless matched
- Per-repo `exclude:` without `--exclude` flag → only per-repo exclusions apply
| `--output` | Output directory | `./hotspot-output` |
| `--hotspot-percentile` | Percentile threshold for hotspot zone | 75 |

### Exclude patterns

Exclude patterns are applied per-language:

| Language | Default exclusions |
|----------|-------------------|
| Python | `__pycache__/*`, `*.pyc`, `.venv/*`, `venv/*`, `build/*`, `dist/*`, `.mypy_cache/*` |
| Java | `target/*`, `build/*`, `.gradle/*`, `generated/*`, `*.class`, `coverage/*` |
| JavaScript | `node_modules/*`, `dist/*`, `build/*`, `*.min.js`, `coverage/*`, `.next/*`, `.angular/*` |
| Default | `.git/*` |

## Output Formats

### ranked.csv

```csv
file_path,churn_score,complexity_score,hotspot_score,commit_count,lines_added,lines_removed,author_count
Hotspot.java,85.00,92.00,88.44,15,420,180,4
Simple.java,5.00,10.00,7.07,2,15,3,1
```

### ranked.md

```markdown
# Hotspot Analysis Report

**Total files:** 150 | **Hotspots:** 12 (8%)

| File | Churn | Complexity | Hotspot | Commits | Authors |
|------|-------|------------|---------|---------|---------|
| Hotspot.java | 85.0 | 92.0 | 88.4 | 15 | 4 |
| ...
```

### scatter.png

X-axis: normalized churn score (0–100)
Y-axis: normalized complexity score (0–100)

- **Blue dots**: normal files
- **Red diamonds**: hotspot zone (top-right quadrant, above both medians)
- Dashed gray lines: median thresholds

### report.html

Interactive HTML generated with Plotly:
- Hover tooltips show file path, scores, and commit details
- Files are colored by hotspot classification
- Sortable columns in the ranked table

### consolidated.html (multi-repo only)

Single self-contained HTML document with:
- Run-level summary (total repos, files, hotspots)
- Per-repo sections with summary stats, file tables, and top-3 hotspot callouts
- Combined ranked table (all files across all repos)
- Failed repos section with error information
- Repos ranked by max hotspot score

## Architecture

```
models/data.py        — FileInfo, RankedResult, RunResult dataclasses
scorer/
├── normalize.py      — IQR-based min-max normalization
├── aggregate.py      — Geometric mean hotspot scoring
└── rank.py           — Percentile-based hotspot flagging
git_analyzer/
├── fetch_files.py    — git ls-files with include/exclude filtering
└── fetch_churn.py    — git log --numstat parsing
complexity_analyzer/
└── lizard_wrapper.py — lizard --csv parsing + file-level aggregation
report/
├── tables.py         — CSV and Markdown generation
├── png_report.py     — matplotlib scatter plot
├── html_report.py    — plotly interactive HTML
└── aggregate.py      — Cross-repo combined reports
    consolidated.py   — Management-facing consolidated HTML
config.py             — Default exclude patterns, threshold config
main.py               — CLI entry point, analysis pipeline orchestration
```

## Data Flow

```
1. git ls-files → file list (filtered by include/exclude)
2. git log --numstat → per-file churn stats
3. lizard --csv → per-file complexity
4. normalize_churn() + normalize_complexity() → 0–100 scores
5. √(churn × complexity) → hotspot score
6. rank_files(percentile) → flag hotspot zone
7. Write CSV, MD, PNG, HTML outputs
```

## Test Suite

```bash
# Run all tests
PYTHONPATH=. .venv/bin/pytest tests/ -v

# Run only report tests
PYTHONPATH=. .venv/bin/pytest tests/test_report.py -v

# Run only aggregate tests
PYTHONPATH=. .venv/bin/pytest tests/test_aggregate.py -v

# Run with coverage
PYTHONPATH=. .venv/bin/pytest tests/ --cov=. --cov-report=term-missing
```

**Current: 38 tests passing**

| Test Module | Tests | Coverage |
|-------------|-------|----------|
| test_git_churn.py | 3 | churn parsing, multi-author, empty |
| test_git_files.py | 5 | all/exclude patterns, combined |
| test_lizard_complexity.py | 2 | CSV parsing, empty input |
| test_scorer.py | 10 | normalization, outlier capping, ranking |
| test_report.py | 8 | CSV, MD, PNG, HTML output |
| test_aggregate.py | 5 | combined CSV/MD, repo aggregation |
| test_repo_list.py | 9 | repo-list parsing, per-repo patterns |
| test_consolidated.py | 3 | consolidated HTML |
| test_smoke.py | 1 | end-to-end with real git repo |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All repos processed successfully |
| 1 | Some repos failed (partial success) |
| 2 | Fatal error (invalid arguments, missing tool) |

## FAQ

**Q: Why are all hotspot scores 0.0?**
A: This happens when a repo has only one commit or all files have identical churn values. Normalization requires variation to produce a scale. Run against a larger codebase with historical git activity.

**Q: Lizard doesn't detect complexity in my file.**
A: Lizard needs multi-line function bodies with actual code blocks (if/switch/try). Single-line compound statements like `if(x>40){ if(x>41){ } }` may be skipped. Use multi-line formatting with proper indentation.

**Q: How do I customize include/exclude patterns?**
A: Two levels of control:
1. **Global**: `--include "*.java" --exclude "build/*"` applies to all repos
2. **Per-repo** (repo-list only): `/path/to/repo include:*.kt exclude:gen/*` replaces global for that repo

**Q: Why was pandas removed?**
A: The tool uses only `lizard`, `matplotlib`, and `plotly`. Pandas was listed but never used.

**Q: Can I run this in CI?**
A: Yes. Add `--output ./hotspot-results` and check the exit code. Exit 0 = all clean, exit 1 = partial (some repos failed). Use `--hotspot-percentile 90` to lower sensitivity.

## License

Internal use only.
