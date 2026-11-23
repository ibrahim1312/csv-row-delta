# CSV Row Delta

Compare two CSV exports by a unique key and report added, removed, and edited records.

## Quick start

Requires Python 3.11 or later. Uses the standard library and runs locally.

```bash
python3 tool.py old.csv new.csv --key id
```

Output is formatted JSON on standard output. Invalid inputs report an error on standard error and exit with status 1. Run the tool with --help for all arguments.

Rows and columns may be reordered. An absent column is reported as null and an empty cell as an empty string. Duplicate or empty keys are rejected.

## Example input

**old.csv**

```
id,name
1,Old
2,Remove
```

**new.csv**

```
name,id
New,1
Add,3
```

## Example output

```json
{
  "added": [
    "3"
  ],
  "removed": [
    "2"
  ],
  "changed": {
    "1": {
      "name": [
        "Old",
        "New"
      ]
    }
  }
}
```

## License

[MIT](LICENSE).
