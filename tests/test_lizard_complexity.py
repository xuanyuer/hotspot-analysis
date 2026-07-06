from unittest.mock import patch, MagicMock
from complexity_analyzer.lizard_wrapper import compute_complexity


class TestComputeComplexity:
    @patch("complexity_analyzer.lizard_wrapper.subprocess.run")
    def test_parses_lizard_csv(self, mock_run):
        """Parsed complexity data matches lizard --csv output format."""
        # Lizard CSV columns:
        # 0:NLOC 1:CCN 2:token_count 3:parameter_count 4:function_length
        # 5:location 6:filename 7:function_name 8:signature 9:MCC 10:NPath
        mock_output = (
            "50,3,30,2,30,\"a.js@1-30@/tmp/repo/a.js\",\"/tmp/repo/a.js\",\"a.js\",\"a.js()\",3,10\n"
            "100,10,100,5,120,\"MainClass.run@10-130@/tmp/repo/b.java\",\"/tmp/repo/b.java\",\"MainClass.run\",\"run(int)\",10,50\n"
            "20,5,20,1,20,\"MainClass.helper@135-155@/tmp/repo/b.java\",\"/tmp/repo/b.java\",\"MainClass.helper\",\"helper(int)\",5,20\n"
        )
        mock_run.return_value = MagicMock(stdout=mock_output)

        result = compute_complexity("/tmp/repo", ["a.js", "b.java"])

        # a.js: 1 function, CCN=3
        assert result["a.js"]["max_complexity"] == 3
        assert abs(result["a.js"]["avg_complexity"] - 3.0) < 0.01

        # b.java: 2 functions, max CCN=10, avg CCN=7.5
        assert result["b.java"]["max_complexity"] == 10
        assert abs(result["b.java"]["avg_complexity"] - 7.5) < 0.01

    @patch("complexity_analyzer.lizard_wrapper.subprocess.run")
    def test_empty_files_list(self, mock_run):
        """No files → empty result."""
        result = compute_complexity("/tmp/repo", [])

        assert result == {}
