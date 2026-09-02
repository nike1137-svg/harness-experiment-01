import re

LOG_PATH = "sample.log"

# 로그에 섞여 있는 두 가지 타임스탬프 형식을 모두 처리한다.
#  1) 2026-08-28 09:14:02
#  2) 28/Aug/2026:09:18:22
LINE_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}|\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})"
    r"\s+(?P<level>\S+)\s+\[(?P<component>\w+)\]\s+(?P<message>.*)$"
)


def parse_errors(path):
    errors = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            match = LINE_PATTERN.match(line)
            if not match:
                # 레벨 필드가 없는 들여쓴 줄(스택 트레이스 등)은 부가 정보이므로 건너뛴다.
                continue
            if match.group("level") != "ERROR":
                continue
            errors.append(
                (match.group("timestamp"), match.group("component"), match.group("message"))
            )
    return errors


def print_table(errors):
    headers = ["Timestamp", "Component", "Message"]
    rows = [headers] + list(errors)
    widths = [max(len(str(row[i])) for row in rows) for i in range(3)]

    def fmt_row(row):
        return " | ".join(str(row[i]).ljust(widths[i]) for i in range(3))

    print(fmt_row(headers))
    print("-+-".join("-" * w for w in widths))
    for row in errors:
        print(fmt_row(row))
    print(f"\n총 ERROR 건수: {len(errors)}")


if __name__ == "__main__":
    errors = parse_errors(LOG_PATH)
    print_table(errors)
