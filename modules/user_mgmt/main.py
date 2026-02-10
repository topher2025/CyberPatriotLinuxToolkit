import argparse
from .sub_modules import audit, groups, users


def main(datapath="/data/parsed.json", dry_run=False, tests=False):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", "-p", default="/data/parsed.json")
    parser.add_argument("--dry-run", "-d", action="store_true")
    parser.add_argument("--test", "-t", action="store_true")

    args = parser.parse_args()
    main(args.data_path, args.dry_run, args.tests)
