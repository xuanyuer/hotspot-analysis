"""End-to-end smoke test: create real git repo, run analysis, verify output."""

import csv
import subprocess
import tempfile
from pathlib import Path


def _make_hotspot_code(cond_val: int) -> str:
    """Generate hotspot Java code with real complexity (multi-line + switch)."""
    return f"""public class Hotspot {{
    void process(int x) {{
        if (x > {cond_val}) {{
            if (x > {cond_val+1}) {{
                if (x > {cond_val+2}) {{
                    if (x > {cond_val+3}) {{
                        return;
                    }}
                }}
            }}
        }}
    }}
    void validate(int y) {{
        if (y < 0) {{
            return;
        }}
        switch (y) {{
            case 1:
            case 2:
            case 3:
                break;
        }}
    }}
}}
"""


def test_smoke_end_to_end():
    """Create a test git repo with varied churn, run hotspot analysis, verify results."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / "test-repo"
        repo_path.mkdir()

        subprocess.run(["git", "init", "-b", "main"], cwd=repo_path,
                      capture_output=True, check=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"],
                      cwd=repo_path, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"],
                      cwd=repo_path, check=True)

        # Create hotspot file with functions
        hotspot_file = repo_path / "Hotspot.java"
        hotspot_file.write_text(_make_hotspot_code(10))
        subprocess.run(["git", "add", "."], cwd=repo_path, capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", "Initial", "--no-gpg-sign"],
                      cwd=repo_path, capture_output=True, check=True)

        # Modify hotspot file 3 more times (4 total commits)
        for threshold in [20, 30, 40]:
            hotspot_file.write_text(_make_hotspot_code(threshold))
            subprocess.run(["git", "add", "Hotspot.java"], cwd=repo_path,
                          capture_output=True, check=True)
            subprocess.run(["git", "commit", "-m", "Update",
                          "--no-gpg-sign"], cwd=repo_path,
                          capture_output=True, check=True)

        # Create simple file (1 commit, one simple function)
        simple_file = repo_path / "Simple.java"
        simple_file.write_text("public class Simple { public int add(int a, int b) { return a + b; } }")
        subprocess.run(["git", "add", "Simple.java"], cwd=repo_path, capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", "Add Simple", "--no-gpg-sign"],
                      cwd=repo_path, capture_output=True, check=True)



        # Run analysis
        from main import run_analysis

        output_dir = Path(tmpdir) / "output"
        run_analysis(repo_path, [], [], "full", output_dir, 75)

        # Verify CSV output
        csv_path = output_dir / "test-repo" / "ranked.csv"
        assert csv_path.exists(), f"CSV not found: {csv_path}"

        with open(csv_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        file_scores = {r["file_path"]: float(r["hotspot_score"]) for r in rows}


        assert len(rows) == 2, f"Expected 2 files, got {len(rows)}"
        assert file_scores["Hotspot.java"] > 0, \
            f"Hotspot.java should have non-zero score, got {file_scores['Hotspot.java']}"

        # Hotspot should be the top file
        top_file = max(file_scores, key=file_scores.get)
        assert top_file == "Hotspot.java", \
            f"Hotspot.java should be top, got {top_file} (scores: {file_scores})"

        # Verify MD output
        md_path = output_dir / "test-repo" / "ranked.md"
        assert md_path.exists(), f"MD not found: {md_path}"

        content = md_path.read_text()
        assert "Hotspot Analysis Report" in content
        assert "Hotspot.java" in content

        print("Smoke test PASSED")
