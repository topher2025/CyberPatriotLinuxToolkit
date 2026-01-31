import os
from logging import exception


def find_readme():
    filenames = ["README.md", "README.txt", "README"]
    basedirs = ["~/Desktop", "~/Documents", "~/Downloads", "."]

    try:
        for base in basedirs:
            path = os.path.normpath(os.path.expanduser(base))
            for filename in filenames:
                if os.path.exists(os.path.join(path, filename)):
                    path = os.path.join(path, filename)
                    if os.path.isfile(path):
                        return os.path.abspath(path)

            for item in os.listdir(os.path.normpath(os.path.expanduser(base))):
                path = os.path.normpath(os.path.expanduser(os.path.join(base, item)))
                if os.path.isdir(path):
                    for filename in filenames:
                        if os.path.exists(os.path.join(path, filename)):
                            path = os.path.join(path, filename)
                            if os.path.isfile(path):
                                return os.path.abspath(path)
    except Exception as e:
        print(f"error: {e}.\nThis is custom output")
    return None


def confirm_path(path):
    return path and os.path.isfile(path) and os.path.basename(path).upper().startswith("README")


def parse_readme(path):
    return "./parsed.json", True