from unittest.mock import patch, MagicMock
from git_analyzer.fetch_churn import compute_churn


class TestComputeChurn:
    @patch("git_analyzer.fetch_churn.subprocess.run")
    def test_parses_commits_correctly(self, mock_run):
        """Parsed churn data matches git log --numstat output."""
        mock_output = (
            "COMMIT_START\naaa111\nAlice\nalice@example.com\n2024-01-01\n"
            "10\t5\ta.js\n"
            "COMMIT_START\ndef456\nBob\nbob@example.com\n2024-01-02\n"
            "3\t1\tb.java\n"
            "COMMIT_START\nbbb222\nAlice\nalice@example.com\n2024-01-03\n"
            "2\t0\ta.js\n"
        )
        mock_run.return_value = MagicMock(stdout=mock_output)

        result = compute_churn("/tmp/repo", "main", ["a.js", "b.java"])

        # a.js: 2 commits (both Alice), 12 added, 5 removed
        assert result["a.js"]["commit_count"] == 2
        assert result["a.js"]["lines_added"] == 12
        assert result["a.js"]["lines_removed"] == 5
        assert result["a.js"]["author_count"] == 1

        # b.java: 1 commit (Bob), 3 added, 1 removed
        assert result["b.java"]["commit_count"] == 1
        assert result["b.java"]["lines_added"] == 3
        assert result["b.java"]["lines_removed"] == 1
        assert result["b.java"]["author_count"] == 1

    @patch("git_analyzer.fetch_churn.subprocess.run")
    def test_multiple_authors(self, mock_run):
        """Distinct authors are counted correctly."""
        mock_output = (
            "COMMIT_START\nabc123\nAlice\nalice@example.com\n2024-01-01\n"
            "10\t5\ta.js\n"
            "COMMIT_START\ndef456\nBob\nbob@example.com\n2024-01-02\n"
            "5\t2\ta.js\n"
            "COMMIT_START\nghi789\nCharlie\ncharlie@example.com\n2024-01-03\n"
            "3\t1\ta.js\n"
        )
        mock_run.return_value = MagicMock(stdout=mock_output)

        result = compute_churn("/tmp/repo", "main", ["a.js"])

        assert result["a.js"]["author_count"] == 3
        assert result["a.js"]["commit_count"] == 3

    @patch("git_analyzer.fetch_churn.subprocess.run")
    def test_empty_files_list(self, mock_run):
        """No files → empty result."""
        result = compute_churn("/tmp/repo", "main", [])

        assert result == {}
