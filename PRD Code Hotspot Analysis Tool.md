# PRD: Code Churn & Complexity Hotspot Analysis Tool

## 1. Background & Problem Statement

Our engineering team is taking ownership of a codebase built by an external vendor. Early review suggests quality concerns, but we need **objective, tool-generated evidence** (not subjective opinion) to support a go/no-go conversation with management before accepting the vendor's delivery.

Code churn/hotspot analysis cross-references two independent, automatically derived signals:
- **Churn**: how frequently a file changes (from git history)
- **Complexity**: how structurally complicated a file is (from static analysis)

Files that are **both high-churn and high-complexity** are "hotspots" — statistically likely to be the highest-risk, highest-maintenance-cost areas of the codebase. This is a well-established technique (popularized by tools like CodeScene, Adam Tornhill's work) but does not require a commercial product to produce a credible first version.

## 2. Goal

Build an internal CLI/script-based tool that:
1. Analyzes git history of a target repository to compute per-file churn metrics
2. Analyzes the same repository for per-file/per-function code complexity
3. Joins both datasets and produces a **hotspot score** per file
4. Outputs a visual report (scatter plot + ranked table) suitable for a management presentation
5. Supports **JS/React** and **Java/Spring Boot** codebases as first-class targets

This tool should be reusable beyond this one vendor engagement — treat it as a general-purpose internal quality assessment utility, not a one-off script.

## 3. Non-Goals

- Not building a full replacement for SonarQube/CodeScene (no historical trend dashboards, no team analytics, no CI/CD gating in v1)
- Not attempting to auto-fix or refactor flagged files
- Not analyzing test coverage or security vulnerabilities (separate existing tooling covers this)
- Not building a persistent web service in v1 — a local CLI tool with file/HTML output is sufficient

## 4. Target Users

- Internal engineering team (primary) — running analysis, interpreting output
- Engineering leadership / management ally — consuming the final report/visualization as evidence in vendor conversations

## 5. Functional Requirements

### 5.1 Input
- Tool accepts **one or more** local paths to git repositories (already cloned) as input:
  - Single repo: `--repo <path>`
  - Multiple repos: repeated `--repo` flags, or a `--repo-list <file>` pointing to a newline/YAML/JSON list of repo paths (useful when scanning an entire vendor's repo set in one run)
  - Each repo entry may optionally specify its own stack override and exclude list, in case a multi-repo run mixes JS/React and Java/Spring Boot projects
- Tool accepts a configurable time window for churn analysis (e.g., `--since=6months`, default: full history), applied uniformly across all repos in the run unless overridden per-repo
- Tool auto-detects stack (JS/TS vs Java) per repo based on file extensions present, or accepts an explicit `--stack` flag (globally or per-repo)
- Tool accepts an optional exclude list (e.g., `node_modules`, `build/`, generated code, vendored dependencies, test fixtures) — should ship with sensible defaults per stack, applied per-repo
- Tool processes repos independently (failure or error in one repo should not abort the full batch — log and continue, report failures in the summary output)

### 5.2 Churn Analysis
- Parse `git log --numstat` (or equivalent) across the specified time window
- For each file, compute:
  - Total number of commits touching the file
  - Total lines added + removed
  - Number of distinct authors (optional secondary signal — high author count + high churn can indicate ownership/consistency issues)
- Normalize churn into a 0–100 relative score per file within the repo

### 5.3 Complexity Analysis
- For **JS/React**: use an existing open-source analyzer (e.g., ESLint with complexity rules, or `escomplex`/`typhonjs-escomplex` successor, or `lizard`) to compute cyclomatic complexity per file/function
- For **Java/Spring Boot**: use an existing open-source analyzer (e.g., `PMD`, `checkstyle` with complexity ruleset, or `lizard`) to compute cyclomatic complexity per file/method
- Aggregate to file-level complexity score (e.g., sum or max of function-level complexity, plus file length as secondary signal)
- Normalize complexity into a 0–100 relative score per file within the repo

### 5.4 Hotspot Scoring
- Join churn score and complexity score per file path
- Compute a combined hotspot score (default: simple product or weighted sum of normalized churn × normalized complexity; weighting should be configurable)
- Rank all files by hotspot score, descending

### 5.5 Optional: Defect Correlation (stretch goal, not v1-blocking)
- Accept an optional CSV/JSON input mapping known bug/incident counts to file paths (manually exported from issue tracker)
- If provided, overlay as a third dimension (bubble size or color) on the visualization, and include in ranked table

### 5.6 Output

**Per-repo outputs** (generated for each repo in the run):
- **Scatter plot** (churn on x-axis, complexity on y-axis, each point = one file, top-right quadrant highlighted as hotspot zone) — exported as a static image (PNG/SVG) and/or interactive HTML
- **Ranked table** (CSV and human-readable Markdown/HTML) listing top N hotspot files with: file path, churn score, complexity score, combined hotspot score, commit count, author count
- **Summary stats**: total files analyzed, % of files in hotspot zone, top 10 hotspots called out explicitly

**Cross-repo aggregate outputs** (generated once per run, when multiple repos are scanned):
- **Combined summary table**: one row per repo, showing file count analyzed, % of files in hotspot zone, average/max hotspot score, and top 3 hotspot files per repo — for quick comparison of which repos/services are riskiest
- **Combined ranked table**: all hotspot files across all repos in one sortable table, with a `repo` column, so the very worst files across the entire vendor delivery can be seen in one view regardless of which repo they live in
- **Run-level report** (single Markdown/HTML doc) bundling the aggregate summary + links/embeds to each per-repo scatter plot and table — this is the artifact intended for the management-facing conversation
- Failed/skipped repos (e.g., not a git repo, unsupported stack, parse errors) listed explicitly in the run-level report rather than silently omitted

All outputs should be self-contained and easy to drop into a slide deck or doc (no live server dependency required to view the plots or tables).

## 6. Non-Functional Requirements

- **Runtime**: should complete analysis of a mid-size repo (~1,000–5,000 files) in under 10 minutes on a standard dev laptop
- **No external network dependency** at analysis time beyond initial tool/dependency installation (important if run against a vendor codebase in a locked-down environment)
- **Language/runtime**: implementation language is flexible (Python recommended for scripting glue + plotting via `matplotlib`/`plotly`, given strong ecosystem support for both git parsing and charting) — but should not require the target repo's own toolchain to be modified
- **No modification** of the target repository (strictly read-only analysis)
- **Reproducibility**: running the tool twice on the same repo/commit should produce identical output

## 7. Proposed Tech Approach (guidance for implementing agent)

| Component | Suggested Approach |
|---|---|
| Git history parsing | `git log --numstat --pretty=format:...` parsed via subprocess, or a library like `GitPython` |
| JS/TS complexity | `lizard` (language-agnostic CLI, supports JS/TS and Java out of the box, low setup friction) as the primary choice; ESLint complexity plugin as fallback if more JS-idiomatic detail needed |
| Java complexity | `lizard` (same tool, keeps pipeline consistent across both stacks) or `PMD` if more Java-specific rule detail is desired |
| Data joining/scoring | Python with `pandas` for normalization, scoring, ranking |
| Visualization | `matplotlib` or `plotly` for scatter plot; `plotly` preferred if interactive HTML output is valuable for stakeholders to explore |
| CLI interface | `argparse` or `click` for a clean interface, e.g.: `python hotspot_analyzer.py --repo <path> --stack java --since 6months` for a single repo, or `python hotspot_analyzer.py --repo-list repos.yaml --since 6months` for a batch run across multiple repos |
| Multi-repo orchestration | Simple sequential loop over repo list in v1 (sufficient given the 10-min-per-repo runtime target); parallelization across repos (e.g., via `multiprocessing` or `concurrent.futures`) can be added later if batch runtime becomes a bottleneck — not required for v1 |

Using `lizard` for both stacks is a deliberate recommendation: it supports both JS/TS and Java (and several other languages) with one consistent tool and output format, which simplifies the pipeline considerably versus maintaining two separate complexity analyzers.

## 8. Deliverables

1. CLI tool (source code + README with setup/usage instructions)
2. Default exclude-pattern configs for JS/React and Java/Spring Boot projects
3. Sample output (scatter plot + ranked table) generated against a test repo, to validate correctness before running against the actual vendor codebase
4. Short usage guide for non-technical stakeholders on how to read the output (1-pager)

## 9. Success Criteria

- Tool runs successfully against both a JS/React and a Java/Spring Boot repository without manual intervention beyond the initial command
- Tool runs successfully across a batch of multiple repos (mixed stacks) in a single invocation, producing both per-repo and cross-repo aggregate outputs
- A single repo failing (bad path, unsupported content, parse error) does not abort the rest of the batch
- Output clearly identifies a ranked list of hotspot files that engineering can independently corroborate as "known problem areas" based on their own code review
- Output is presentable as-is (or with minimal touch-up) in a management-facing document/deck, including the cross-repo view showing which services/repos are riskiest overall
- Total build effort lands within 1–3 engineer-days for v1, per original estimate (multi-repo orchestration is a thin loop over existing single-repo logic, not expected to materially increase build effort)

## 10. Open Questions for Implementation

- Preferred output format priority: is static PNG sufficient, or is interactive HTML (hover tooltips showing file path/scores) valuable enough to prioritize in v1?
- Should the exclude-list be repo-specific config files (e.g., a `.hotspotignore`) or CLI flags only?
- Do we want author-count-per-file included in v1 scoring, or held as a stretch/secondary metric only (per 5.2)?
- Confirm whether defect correlation (5.5) should be pulled into v1 scope or explicitly deferred — depends on how quickly issue-tracker export can be prepared.
