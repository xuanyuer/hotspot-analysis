"""Tests for report/table generation."""

import csv
import os
import tempfile
from pathlib import Path

from hotspot.models.data import FileInfo, RankedResult
from hotspot.report.tables import write_csv_report, write_markdown_report
from hotspot.report.png_report import write_png_scatter
from hotspot.report.html_report import write_html_report


def _make_file(path: str, churn: float, complexity: float,
               hotspot: float, commits: int = 0, authors: int = 0,
               lines_added: int = 0, lines_removed: int = 0) -> FileInfo:
    return FileInfo(
        path=path, churn_score=churn, complexity_score=complexity,
        hotspot_score=hotspot, commit_count=commits, author_count=authors,
        lines_added=lines_added, lines_removed=lines_removed,
    )


class TestWriteCsvReport:
    def test_writes_all_files_sorted_by_score(self):
        files = [
            _make_file("a.java", 10.0, 20.0, 15.0, commits=5, authors=2),
            _make_file("b.java", 50.0, 80.0, 65.0, commits=10, authors=3),
            _make_file("c.java", 90.0, 95.0, 92.0, commits=15, authors=4),
        ]
        result = RankedResult(
            all_files=sorted(files, key=lambda f: f.hotspot_score, reverse=True),
            hotspot_files=[files[2]],
            total_files=3, hotspot_count=1, hotspot_ratio=1/3,
            hotspot_percentile=75,
        )

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            csv_path = Path(f.name)

        write_csv_report(result, str(csv_path))

        with open(csv_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 3
        assert rows[0]["file_path"] == "c.java"
        assert rows[1]["file_path"] == "b.java"
        assert rows[2]["file_path"] == "a.java"
        assert float(rows[0]["hotspot_score"]) == 92.0

    def test_empty_result(self):
        result = RankedResult(
            all_files=[], hotspot_files=[],
            total_files=0, hotspot_count=0, hotspot_ratio=0.0,
            hotspot_percentile=75,
        )

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            csv_path = Path(f.name)

        write_csv_report(result, str(csv_path))

        with open(csv_path) as f:
            rows = list(csv.DictReader(f))

        assert len(rows) == 0

    def test_csv_has_correct_headers(self):
        result = RankedResult(
            all_files=[], hotspot_files=[],
            total_files=0, hotspot_count=0, hotspot_ratio=0.0,
            hotspot_percentile=75,
        )

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            csv_path = Path(f.name)

        write_csv_report(result, str(csv_path))

        with open(csv_path) as f:
            header = f.readline().strip()

        expected = "file_path,churn_score,complexity_score,hotspot_score,commit_count,lines_added,lines_removed,author_count"
        assert header == expected


class TestWriteMarkdownReport:
    def test_writes_all_files_sorted_by_score(self):
        files = [
            _make_file("hot.java", 90.0, 95.0, 92.0, commits=15, authors=4),
            _make_file("simple.java", 10.0, 10.0, 10.0, commits=1, authors=1),
        ]
        result = RankedResult(
            all_files=sorted(files, key=lambda f: f.hotspot_score, reverse=True),
            hotspot_files=files,
            total_files=2, hotspot_count=2, hotspot_ratio=1.0,
            hotspot_percentile=50,
        )

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            md_path = Path(f.name)

        write_markdown_report(result, str(md_path))

        content = md_path.read_text()

        assert "# Hotspot Analysis Report" in content
        assert "**Total files:** 2" in content
        assert "**Hotspots:** 2 (100%)" in content
        assert "| hot.java | 90.0 | 95.0 | 92.0 | 15 | 4 |" in content
        assert "| simple.java | 10.0 | 10.0 | 10.0 | 1 | 1 |" in content

    def test_empty_result_has_no_file_rows(self):
        result = RankedResult(
            all_files=[], hotspot_files=[],
            total_files=0, hotspot_count=0, hotspot_ratio=0.0,
            hotspot_percentile=75,
        )

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            md_path = Path(f.name)

        write_markdown_report(result, str(md_path))

        content = md_path.read_text()

        assert "# Hotspot Analysis Report" in content
        assert "**Total files:** 0" in content
        assert "simple" not in content


class TestWritePngScatter:
    def test_creates_png_file(self):
        files = [
            _make_file("a.java", 10.0, 20.0, 15.0),
            _make_file("b.java", 50.0, 80.0, 65.0),
            _make_file("c.java", 90.0, 95.0, 92.0),
        ]
        result = RankedResult(
            all_files=sorted(files, key=lambda f: f.hotspot_score, reverse=True),
            hotspot_files=[],
            total_files=3, hotspot_count=0, hotspot_ratio=0.0,
            hotspot_percentile=75,
        )

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            png_path = Path(f.name)

        write_png_scatter(result, str(png_path))

        assert png_path.exists()
        assert png_path.stat().st_size > 100  # not empty

    def test_empty_result_no_plot(self):
        result = RankedResult(
            all_files=[], hotspot_files=[],
            total_files=0, hotspot_count=0, hotspot_ratio=0.0,
            hotspot_percentile=75,
        )

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            png_path = Path(f.name)

        write_png_scatter(result, str(png_path))

        assert png_path.exists()
        assert png_path.stat().st_size > 0


class TestWriteHtmlReport:
    def test_creates_html_file(self):
        files = [
            _make_file("a.java", 10.0, 20.0, 15.0),
            _make_file("b.java", 50.0, 80.0, 65.0),
            _make_file("c.java", 90.0, 95.0, 92.0),
        ]
        result = RankedResult(
            all_files=sorted(files, key=lambda f: f.hotspot_score, reverse=True),
            hotspot_files=[],
            total_files=3, hotspot_count=0, hotspot_ratio=0.0,
            hotspot_percentile=75,
        )

        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            html_path = Path(f.name)

        write_html_report(result, str(html_path))

        assert html_path.exists()
        assert html_path.stat().st_size > 500
        content = html_path.read_text()
        assert "Hotspot Analysis" in content
        assert "a.java" in content
        assert "b.java" in content
        assert "c.java" in content

    def test_empty_result(self):
        result = RankedResult(
            all_files=[], hotspot_files=[],
            total_files=0, hotspot_count=0, hotspot_ratio=0.0,
            hotspot_percentile=75,
        )

        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            html_path = Path(f.name)

        write_html_report(result, str(html_path))

        assert html_path.exists()
        assert html_path.stat().st_size > 0
