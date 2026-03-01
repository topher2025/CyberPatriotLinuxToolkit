import os
from datetime import datetime

_interactive = True


def set_interactive(interactive):
    """Set the global interactive mode."""
    global _interactive
    _interactive = interactive


def log_output(output):
    """Log output to console or file based on interactive mode."""
    if _interactive:
        print(output)
    else:
        # Create logs directory if it doesn't exist
        os.makedirs("./logs", exist_ok=True)

        # Use today's date for the log filename
        date = datetime.now().strftime("%Y-%m-%d")
        with open(f"./logs/{date}.txt", "a") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"{timestamp} - {output}\n")
