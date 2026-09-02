import re

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}|\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>\S+)\s+"
    r"\[(?P<component>[^\]]+)\]\s+"
    r"(?P<message>.*)$"
)


def parse_errors(path):
    """로그 파일에서 레벨이 ERROR인 줄만 추출한다.

    Args:
        path: 로그 파일 경로

    Returns:
        dict 리스트. 각 dict는 timestamp/component/message 키를 가진다.
    """
    errors = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            match = LOG_PATTERN.match(line)
            if not match:
                continue
            if match.group("level") != "ERROR":
                continue
            errors.append(
                {
                    "timestamp": match.group("timestamp"),
                    "component": match.group("component"),
                    "message": match.group("message"),
                }
            )
    return errors


def print_table(errors):
    headers = ["timestamp", "component", "message"]
    widths = {h: len(h) for h in headers}
    for e in errors:
        for h in headers:
            widths[h] = max(widths[h], len(e[h]))

    def fmt_row(values):
        return " | ".join(v.ljust(widths[h]) for h, v in zip(headers, values))

    print(fmt_row(headers))
    print("-+-".join("-" * widths[h] for h in headers))
    for e in errors:
        print(fmt_row([e["timestamp"], e["component"], e["message"]]))
    print(f"\n총 ERROR 건수: {len(errors)}")


if __name__ == "__main__":
    errors = parse_errors("sample.log")
    print_table(errors)
