import csv
import json
import sys
from statistics import mean, median


def is_number(value):
    if value is None:
        return False
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def summarize_column(values):
    non_empty = [v for v in values if v is not None and str(v).strip() != ""]
    numeric = [v for v in non_empty if is_number(v)]
    if numeric:
        nums = [float(v) for v in numeric]
        return {
            "type": "numeric",
            "count": len(nums),
            "min": min(nums),
            "max": max(nums),
            "mean": round(mean(nums), 6),
            "median": round(median(nums), 6),
        }
    if non_empty:
        return {
            "type": "text",
            "count": len(non_empty),
            "unique": len(set(str(v) for v in non_empty)),
        }
    return {"type": "empty", "count": 0}


def main(argv):
    if len(argv) < 2:
        print("Usage: python main.py <file.csv> [--pretty]", file=sys.stderr)
        return 2
    path = argv[1]
    pretty = "--pretty" in argv[2:]
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        print(json.dumps({"columns": {}, "row_count": 0}))
        return 0
    header = rows[0]
    data = rows[1:]
    columns = {name: [] for name in header}
    for row in data:
        for i, name in enumerate(header):
            columns[name].append(row[i] if i < len(row) else "")
    summary = {name: summarize_column(vals) for name, vals in columns.items()}
    result = {"row_count": len(data), "columns": summary}
    if pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))