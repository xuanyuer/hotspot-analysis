from unittest.mock import patch, MagicMock
from pathlib import Path
from git_analyzer.fetch_files import fetch_files


class TestFetchFiles:
    @patch("git_analyzer.fetch_files.subprocess.run")
    def test_returns_all_files_when_no_filters(self, mock_run):
        mock_run.return_value = MagicMock(stdout="a.js\nb.java\nc.py\n")
        result = fetch_files(Path("/tmp/repo"), "main", [], [])

        assert result == ["a.js", "b.java", "c.py"]
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert "git" in call_args[0][0]
        assert "ls-files" in call_args[0][0]

    @patch("git_analyzer.fetch_files.subprocess.run")
    def test_excludes_patterns(self, mock_run):
        mock_run.return_value = MagicMock(stdout="a.js\nb.js\nc.js\ntest.js\n")
        result = fetch_files(Path("/tmp/repo"), "main", [], ["*.js", "test.js"])

        assert result == []

    @patch("git_analyzer.fetch_files.subprocess.run")
    def test_includes_patterns(self, mock_run):
        mock_run.return_value = MagicMock(stdout="a.js\nb.js\nc.py\n")
        result = fetch_files(Path("/tmp/repo"), "main", ["*.js"], [])

        assert result == ["a.js", "b.js"]

    @patch("git_analyzer.fetch_files.subprocess.run")
    def test_include_and_exclude_combined(self, mock_run):
        mock_run.return_value = MagicMock(stdout="src/a.js\ntest/a.js\ndocs/b.md\ntest/c.py\n")
        result = fetch_files(Path("/tmp/repo"), "main", ["*.js"], ["test/*"])

        assert result == ["src/a.js"]

    @patch("git_analyzer.fetch_files.subprocess.run")
    def test_empty_repo(self, mock_run):
        mock_run.return_value = MagicMock(stdout="")
        result = fetch_files(Path("/tmp/repo"), "main", [], [])

        assert result == []
