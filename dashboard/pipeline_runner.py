from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent


def run_pipeline():
    """
    Runs the complete ETL + database + analytics pipeline.
    Returns:
        success: bool
        output: str
    """

    pipeline_path = PROJECT_ROOT.parent / "etl" / "run_pipeline.py"

    result = subprocess.run(
        [sys.executable, str(pipeline_path)],
        cwd=PROJECT_ROOT.parent,
        capture_output=True,
        text=True
    )

    output = result.stdout

    if result.stderr:
        output += "\n\nERRORS / WARNINGS:\n" + result.stderr

    return result.returncode == 0, output