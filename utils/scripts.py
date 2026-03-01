import subprocess
from pathlib import Path


def run_script(script_path: str, *args, cwd: str = None, sudo: bool = False) -> dict:
    """
    Runs a shell script and returns its output.

    Args:
        script_path (str): Path to the shell script (absolute or relative to cwd).
        *args: Arguments to pass to the shell script.
        cwd (str, optional): Directory to run the script from. Defaults to None.
        sudo (bool, optional): Whether to run the script with sudo. Defaults to False.

    Returns:
        dict: Contains 'stdout', 'stderr', and 'returncode'.
    """
    script_path_obj = Path(script_path)

    # Check if script exists - if cwd is provided, check relative to cwd
    if cwd:
        full_path = Path(cwd) / script_path
    else:
        full_path = script_path_obj

    if not full_path.exists():
        raise FileNotFoundError(f"Script not found: {full_path}")

    # Build command with optional sudo
    cmd = []
    if sudo:
        cmd.extend(["sudo", "-n"])  # -n flag for non-interactive (passwordless)
    cmd.extend(["bash", str(full_path), *args])

    # Run the script
    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": result.returncode,
    }


def run_script_stdout(
    script_path: str, *args, cwd: str = None, sudo: bool = False
) -> str:
    """
    Runs a shell script and returns its standard output.

    Args:
        script_path (str): Path to the shell script (absolute or relative to cwd).
        *args: Arguments to pass to the shell script.
        cwd (str, optional): Directory to run the script from. Defaults to None.
        sudo (bool, optional): Whether to run the script with sudo. Defaults to False.
    """
    result = run_script(script_path, *args, cwd=cwd, sudo=sudo)
    if result["returncode"] != 0:
        raise RuntimeError(f"Script failed with error: {result['stderr']}")
    return result["stdout"]


def run_line(command: str, cwd: str = None, sudo: bool = False) -> dict:
    """
    Runs a shell command line and returns its output.

    Args:
        command (str): The shell command to run.
        cwd (str, optional): Directory to run the command from. Defaults to None.
        sudo (bool, optional): Whether to run the command with sudo. Defaults to False.

    Returns:
        dict: Contains 'stdout', 'stderr', and 'returncode'.
    """
    cmd = []
    if sudo:
        cmd.extend(["sudo", "-n"])  # -n flag for non-interactive (passwordless)
    cmd.extend(["bash", "-c", command])

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)

    return {
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": result.returncode,
    }
