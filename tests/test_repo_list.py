"""Tests for repo-list parsing with per-repo patterns."""

import tempfile
from pathlib import Path

from git_analyzer.repo_list import parse_repo_list, RepoEntry


def _write_repo_list(content: str) -> str:
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
    tmp.write(content)
    tmp.close()
    return tmp.name


class TestParseRepoList:
    def test_simple_paths(self):
        path = _write_repo_list("/path/a\n/path/b\n")
        entries = parse_repo_list(path, [], [])

        assert len(entries) == 2
        assert entries[0].path == Path("/path/a")
        assert entries[0].include_patterns == []
        assert entries[1].path == Path("/path/b")

    def test_comments_and_empty_lines(self):
        path = _write_repo_list("# comment\n\n/path/a\n\n# another\n/path/b\n")
        entries = parse_repo_list(path, [], [])

        assert len(entries) == 2
        assert entries[0].path == Path("/path/a")
        assert entries[1].path == Path("/path/b")

    def test_per_repo_include_override_global(self):
        path = _write_repo_list("/path/a include:*.java include:*.kt\n/path/b\n")
        entries = parse_repo_list(path, ["*.py"], [])

        assert entries[0].include_patterns == ["*.java", "*.kt"]
        assert entries[1].include_patterns == ["*.py"]  # falls back to global

    def test_per_repo_exclude_override_global(self):
        path = _write_repo_list("/path/a exclude:build/* exclude:gen/*\n/path/b\n")
        entries = parse_repo_list(path, [], ["*.pyc"])

        assert entries[0].exclude_patterns == ["build/*", "gen/*"]
        assert entries[1].exclude_patterns == ["*.pyc"]

    def test_per_repo_include_replaces_global_include(self):
        path = _write_repo_list("/path/a include:*.java\n")
        entries = parse_repo_list(path, ["*.py", "*.kt"], [])

        # Per-repo include replaces global, not merges
        assert entries[0].include_patterns == ["*.java"]
        assert "*.py" not in entries[0].include_patterns

    def test_per_repo_empty_exclude_keeps_global_exclude(self):
        path = _write_repo_list("/path/a include:*.java\n")
        entries = parse_repo_list(path, [], ["*.pyc"])

        assert entries[0].include_patterns == ["*.java"]
        assert entries[0].exclude_patterns == ["*.pyc"]  # global kept

    def test_multiple_inline_patterns_same_line(self):
        path = _write_repo_list("/path/a include:*.java include:*.kt exclude:build/* exclude:gen/*\n")
        entries = parse_repo_list(path, [], [])

        assert entries[0].include_patterns == ["*.java", "*.kt"]
        assert entries[0].exclude_patterns == ["build/*", "gen/*"]

    def test_global_patterns_for_no_per_repo(self):
        path = _write_repo_list("/path/a\n/path/b\n")
        entries = parse_repo_list(path, ["include:*.java"], ["exclude:build/*"])

        assert entries[0].include_patterns == ["include:*.java"]
        assert entries[0].exclude_patterns == ["exclude:build/*"]

    def test_unknown_token_ignored(self):
        path = _write_repo_list("/path/a include:*.java unknown_token exclude:build/*\n")
        entries = parse_repo_list(path, [], [])

        assert entries[0].include_patterns == ["*.java"]
        assert entries[0].exclude_patterns == ["build/*"]
