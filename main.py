import argparse
from utils import readme
from modules.user_mgmt import main


#########################################
### Override error() to suppress help ###
#########################################
class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"Error: {message}")


parser = argparse.ArgumentParser(
    description="CyberPatriot Automation Script for Linux.",
    epilog="Developed by Christopher Lewis, 2026.",
)

#########################################
###            README Args            ###
#########################################
parser.add_argument(
    "--readme", "-r", metavar="FILE", help="Path to competition README file"
)
parser.add_argument(
    "--auto-readme",
    "-R",
    action="store_true",
    help="Auto-find README in common locations",
)
parser.add_argument(
    "--parse-readme",
    "-P",
    action="store_true",
    help="Only parse and display README data",
)
#########################################
###            Other  Args            ###
#########################################
parser.add_argument(
    "--dry-run", "-d", action="store_true", help="Preview changes without applying"
)

parser.add_argument(
    "--no-interactive",
    "-y",
    action="store_false",
    dest="interactive",
)
parser.add_argument(
    "--password-policy", "-p", action="store_true", help="Password policy enforcement"
)
parser.add_argument(
    "--account-permissions",
    "-a",
    action="store_true",
    help="Account permissions check (requires README)",
)
parser.add_argument(
    "--user-management",
    "-u",
    action="store_true",
    help="User management (requires README)",
)
parser.add_argument(
    "--service-management", "-s", action="store_true", help="Service management"
)
parser.add_argument(
    "--audit-policy", "-t", action="store_true", help="Audit policy configuration"
)
parser.add_argument(
    "--firewall", "-f", action="store_true", help="Firewall configuration"
)
parser.add_argument(
    "--security-hardening", "-k", action="store_true", help="Security hardening"
)
parser.add_argument(
    "--media-scan", "-m", action="store_true", help="Prohibited media scanner"
)
parser.add_argument("--all", action="store_true", help="Run all tasks")


if __name__ == "__main__":
    args = parser.parse_args()
    r_path = ""

    # Readme Status
    r_status = False
    if args.parse_readme or args.all:
        if args.readme and args.auto_readme:
            parser.error("You can't specify both --readme and --auto-readme")
        else:
            if args.readme:
                r_path = args.readme
                if readme.confirm_path(r_path):
                    r_status = True
                else:
                    parser.error(
                        "Could not find README file: Provided path was not found"
                    )
            elif args.auto_readme or args.all:
                r_path = readme.find_readme()
                if r_path and readme.confirm_path(r_path):
                    r_status = True
                else:
                    parser.error("Could not find README file")
        if not r_status:
            parser.error("Unknown README file error caught")

    if (args.parse_readme or args.all) and r_status:
        parsed_readme, r_status = readme.parse_readme(path=r_path)
        pass
    else:
        r_status = False

    if args.password_policy or args.all:
        pass
    if args.account_permissions or args.all:
        if not r_status:
            parser.error("Account permissions require README file")
        else:
            pass
    if args.user_management or args.all:
        if not r_status:
            parser.error("User permissions require README file")
        else:
            pass
    if args.service_management or args.all:
        pass
    if args.audit_policy or args.all:
        pass
    if args.firewall or args.all:
        pass
    if args.security_hardening or args.all:
        pass
    if args.media_scan or args.all:
        pass
