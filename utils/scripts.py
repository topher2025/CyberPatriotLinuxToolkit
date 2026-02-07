import subprocess
from pathlib import Path


def run_script(script_path: str, *args, cwd: str = None) -> dict:
    """
    Runs a shell script and returns its output.

    Args:
        script_path (str): Path to the shell script (absolute or relative to cwd).
        *args: Arguments to pass to the shell script.
        cwd (str, optional): Directory to run the script from. Defaults to None.

    Returns:
        dict: Contains 'stdout', 'stderr', and 'returncode'.
    """
    script_path = Path(script_path)

    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    # Run the script
    result = subprocess.run(
        ["bash", str(script_path), *args],
        capture_output=True,
        text=True,
        cwd=cwd
    )

    return {
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": result.returncode
    }
