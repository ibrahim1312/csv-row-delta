"""Compare two CSV exports by a unique key and report added, removed, and edited records."""

import argparse
import json
from decimal import InvalidOperation
from pathlib import Path
import csv


def main():
    parser = argparse.ArgumentParser(description='Compare two CSV exports by a unique key and report added, removed, and edited records.')
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--key", required=True)
    args = parser.parse_args()

    def load(path):
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, strict=True)
            fields = reader.fieldnames or []
            if args.key not in fields or len(set(fields)) != len(fields):
                raise ValueError(f"{path}: key must exist and headers must be unique")
            rows = {}
            for row in reader:
                if None in row or None in row.values():
                    raise ValueError(f"{path}:{reader.line_num}: wrong number of columns")
                key = row[args.key]
                if not key.strip() or key in rows:
                    raise ValueError(f"{path}:{reader.line_num}: empty or duplicate key")
                rows[key] = row
            return rows

    before, after = load(args.before), load(args.after)
    changed = {}
    for key in sorted(before.keys() & after.keys()):
        old, new = before[key], after[key]
        edits = {field: [old.get(field), new.get(field)]
                 for field in sorted(old.keys() | new.keys()) if old.get(field) != new.get(field)}
        if edits:
            changed[key] = edits
    report = {"added": sorted(after.keys() - before.keys()),
              "removed": sorted(before.keys() - after.keys()), "changed": changed}
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, OverflowError, InvalidOperation, TypeError, csv.Error) as error:
        raise SystemExit(f"Error: {error}") from None
