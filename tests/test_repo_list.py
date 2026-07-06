"""Tests for YAML config file parsing."""

import tempfile
from pathlib import Path

import pytest

from hotspot.git_analyzer.repo_list import parse_config, RepoEntry


def _write_yaml(content: str) -> str:
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
    tmp.write(content)
    tmp.close()
    return tmp.name


class TestParseConfig:
    def test_parse_global_defaults(self, tmp_path: Path):
        (tmp_path / "repo_a").mkdir()
        (tmp_path / "repo_b").mkdir()

        config = _write_yaml(f"""global:
  include: ["*.java", "*.kt"]
  exclude: ["target/*", "build/*"]
repos:
  {tmp_path / 'repo_a'}:
  {tmp_path / 'repo_b'}:
""")
        entries = parse_config(config)

        assert len(entries) == 2
        assert entries[0].path == tmp_path / "repo_a"
        assert entries[0].include_patterns == ["*.java", "*.kt"]
        assert entries[0].exclude_patterns == ["target/*", "build/*"]
        assert entries[1].path == tmp_path / "repo_b"
        assert entries[1].include_patterns == ["*.java", "*.kt"]
        assert entries[1].exclude_patterns == ["target/*", "build/*"]

    def test_per_repo_override_replaces_global(self, tmp_path: Path):
        (tmp_path / "repo_a").mkdir()
        (tmp_path / "repo_b").mkdir()

        config = _write_yaml(f"""global:
  include: ["*.java", "*.kt"]
  exclude: ["target/*"]
repos:
  {tmp_path / 'repo_a'}:
    include: ["*.js", "*.ts"]
    exclude: ["node_modules/*"]
  {tmp_path / 'repo_b'}:
""")
        entries = parse_config(config)

        # /path/a overrides replace global — not merged
        assert entries[0].include_patterns == ["*.js", "*.ts"]
        assert entries[0].exclude_patterns == ["node_modules/*"]
        # /path/b inherits global
        assert entries[1].include_patterns == ["*.java", "*.kt"]
        assert entries[1].exclude_patterns == ["target/*"]

    def test_missing_repo_path_raises_error(self):
        path = _write_yaml("""global:
  include: ["*.java"]
repos:
  /nonexistent/repo:
""")
        with pytest.raises(FileNotFoundError) as exc_info:
            parse_config(path)

        assert "/nonexistent/repo" in str(exc_info.value)

    def test_comments_ignored(self, tmp_path: Path):
        (tmp_path / "repo").mkdir()

        config = _write_yaml(f"""# This is a comment
# Another comment
global:
  include: ["*.java"]
  exclude: ["target/*"]
# Comment between sections
repos:
  # Comment before entry
  {tmp_path / 'repo'}:
    # Comment before override
    include: ["*.kt"]
""")
        entries = parse_config(config)

        assert len(entries) == 1
        assert entries[0].include_patterns == ["*.kt"]
        assert entries[0].exclude_patterns == ["target/*"]

    def test_repo_order_preserved(self, tmp_path: Path):
        (tmp_path / "aaa").mkdir()
        (tmp_path / "zzz").mkdir()
        (tmp_path / "mmm").mkdir()

        config = _write_yaml(f"""repos:
  {tmp_path / 'zzz'}:
  {tmp_path / 'aaa'}:
  {tmp_path / 'mmm'}:
""")
        entries = parse_config(config)

        assert [e.path.name for e in entries] == ["zzz", "aaa", "mmm"]

    def test_auto_discover_repos_yaml(self, tmp_path: Path, monkeypatch):
        (tmp_path / "repo").mkdir()
        (tmp_path / "repos.yaml").write_text(f"""global:
  include: ["*.java"]
repos:
  {tmp_path / 'repo'}:
""")

        monkeypatch.chdir(tmp_path)
        entries = parse_config()

        assert len(entries) == 1
        assert entries[0].include_patterns == ["*.java"]

    def test_empty_repos_section(self):
        path = _write_yaml("""global:
  include: ["*.java"]
repos: {}
""")
        entries = parse_config(path)

        assert len(entries) == 0
