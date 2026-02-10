import os
import re
import json
import html


def find_readme():
    filenames = ["README.md", "README.txt", "README", "README.html"]
    basedirs = [".", "~/Desktop", "~/Documents", "~/Downloads"]

    try:
        for base in basedirs:
            path = os.path.normpath(os.path.expanduser(base))
            for filename in filenames:
                if os.path.exists(os.path.join(path, filename)):
                    path = os.path.join(path, filename)
                    if os.path.isfile(path):
                        if confirm_path(path):
                            return os.path.abspath(path)

            for item in os.listdir(os.path.normpath(os.path.expanduser(base))):
                path = os.path.normpath(os.path.expanduser(os.path.join(base, item)))
                if os.path.isdir(path):
                    for filename in filenames:
                        if os.path.exists(os.path.join(path, filename)):
                            path = os.path.join(path, filename)
                            if os.path.isfile(path):
                                if confirm_path(path):
                                    return os.path.abspath(path)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"error: {e}.")
    return None


def confirm_path(path):
    return (
        path
        and os.path.isfile(path)
        and os.path.basename(str(path)).upper().startswith("README")
        and not ignore_readme(path)
    )


def strip_html(text: str) -> str:
    text = re.sub(r"<script.*?>.*?</script>", "", text, flags=re.I | re.S)
    text = re.sub(r"<style.*?>.*?</style>", "", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = html.unescape(text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def is_valid_username(name: str) -> bool:
    if not name:
        return False
    if len(name) > 50:
        return False
    low = name.lower()
    if any(x in low for x in ("password", "authorized", "services", ":")):
        return False
    return re.fullmatch(r"[a-zA-Z0-9._-]+", name) is not None


def ignore_readme(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            # print(first_line)
            # Return False if 'IGNORE' is in the first line
            return "<!-- IGNORE -->" == first_line
    except FileNotFoundError:
        # File doesn't exist, treat as not ignored
        return True


def parse_readme(path: str):
    os.makedirs("data", exist_ok=True)

    try:
        if not os.path.exists(path):
            raise FileNotFoundError(path)

        raw = open(path, "r", encoding="utf-8", errors="ignore").read()
        plain = strip_html(raw)

        data = {
            "users": [],
            "admins": [],
            "required_services": [],
            "add_groups": {},
            "add_users": [],
        }

        # -----------------------------
        # AUTHORIZED ADMINS / USERS
        # -----------------------------
        auth_match = re.search(
            r"Authorized Administrators and Users(.*?)(Competition Guidelines|ANSWER KEY)",
            plain,
            re.I | re.S,
        )

        if auth_match:
            block = auth_match.group(1)

            current = None
            for line in block.splitlines():
                line = line.strip()
                if not line:
                    continue

                low = line.lower()

                if "authorized administrators" in low:
                    current = "admin"
                    continue

                if "authorized users" in low:
                    current = "user"
                    continue

                if low.startswith("password"):
                    continue

                name = re.sub(r"\(you\)", "", line).strip()

                if is_valid_username(name):
                    if current == "admin" and name not in data["admins"]:
                        data["admins"].append(name)
                    elif current == "user" and name not in data["users"]:
                        data["users"].append(name)

        # -----------------------------
        # USERS TO ADD
        # -----------------------------
        user_patterns = [
            r"(?:make|create)\s+(?:a\s+)?(?:new\s+)?(?:user|account).*?"
            r"(?:named|called)\s+['\"]?([a-zA-Z0-9._-]+)['\"]?"
        ]

        for pat in user_patterns:
            for m in re.finditer(pat, plain, re.I | re.S):
                user = m.group(1).strip("\"'")

                if is_valid_username(user) and user not in data["add_users"]:
                    data["add_users"].append(user)

        # -----------------------------
        # GROUP CREATION
        # -----------------------------
        group_pattern = (
            r"(?:make|create)\s+(?:a\s+)?(?:new\s+)?group\s+"
            r"(?:called\s+)?['\"]?(\w+)['\"]?"
            r".*?:\s*([a-zA-Z0-9_,\s]+)\."
        )

        for m in re.finditer(group_pattern, plain, re.I | re.S):
            group = m.group(1)
            members_raw = m.group(2)

            members = []
            for token in re.split(r"[,\s]+", members_raw):
                token = token.strip(",. ")
                if is_valid_username(token):
                    members.append(token)

            if members:
                data["add_groups"][group] = members

        # -----------------------------
        # CRITICAL SERVICES (FIXED)
        # -----------------------------
        services_match = re.search(
            r"Critical Services\s*(.*?)(?:Authorized Administrators|Competition Guidelines|$)",
            plain,
            re.I | re.S,
        )

        if services_match:
            block = services_match.group(1)

            for line in block.splitlines():
                line = line.strip()

                # Skip junk
                if not line:
                    continue
                if line.lower().startswith("critical services"):
                    continue
                if line in (".", "-", "*"):
                    continue
                if "none" in line.lower():
                    continue

                # Must contain at least one letter
                if not re.search(r"[a-zA-Z]", line):
                    continue

                data["required_services"].append(line)

        # -----------------------------
        # WRITE OUTPUT
        # -----------------------------
        out_path = "data/parsed.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return out_path, True

    except Exception as e:
        err_path = "data/error_encountered.json"
        with open(err_path, "w", encoding="utf-8") as f:
            json.dump({"error": str(e)}, f, indent=2)

        return err_path, False
