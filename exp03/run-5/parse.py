import re

LOG_FILE = "sample.log"

# 타임스탬프(형식 무관) + LEVEL + [컴포넌트] + 메시지 구조를 파싱
LINE_PATTERN = re.compile(
    r"^(?P<ts>\S.*?)\s+(?P<level>INFO|WARN|ERROR|DEBUG)\s+\[(?P<comp>\w+)\]\s+(?P<msg>.*)$"
)


def parse_errors(path):
    errors = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            match = LINE_PATTERN.match(line.rstrip("\n"))
            if match and match.group("level") == "ERROR":
                errors.append(
                    (match.group("ts"), match.group("comp"), match.group("msg"))
                )
    return errors


def print_table(rows):
    headers = ("시간", "컴포넌트", "메시지")
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt_row(cells):
        return " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells))

    print(fmt_row(headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(fmt_row(row))


if __name__ == "__main__":
    errors = parse_errors(LOG_FILE)
    print(f"총 {len(errors)}건의 ERROR 발견\n")
    print_table(errors)
