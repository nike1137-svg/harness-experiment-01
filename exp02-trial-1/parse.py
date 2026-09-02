#!/usr/bin/env python3
import re
import sys

LOG_FILE = "sample.log"

# 두 가지 타임스탬프 형식(YYYY-MM-DD HH:MM:SS, DD/Mon/YYYY:HH:MM:SS)을 모두 인식한다.
LINE_PATTERN = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}|\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2})"
    r"\s+(?P<level>INFO|WARN|ERROR)\s+\[(?P<module>[^\]]+)\]\s+(?P<message>.*)$"
)


def parse_errors(path):
    errors = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = LINE_PATTERN.match(line.strip())
            if m and m.group("level") == "ERROR":
                errors.append((m.group("ts"), m.group("module"), m.group("message")))
    return errors


def print_table(rows):
    headers = ("TIMESTAMP", "MODULE", "MESSAGE")
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(val))

    def fmt_row(values):
        return " | ".join(v.ljust(widths[i]) for i, v in enumerate(values))

    print(fmt_row(headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(fmt_row(row))


if __name__ == "__main__":
    rows = parse_errors(LOG_FILE)
    if not rows:
        print(f"{LOG_FILE} 에서 ERROR 로그를 찾지 못했습니다.")
        sys.exit(0)
    print_table(rows)
    print(f"\n총 {len(rows)}건의 ERROR 발견")
