import re

LOG_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<level>\S+)\s+(?P<message>.*)$"
)


def parse_errors(log_path):
    errors = []
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            match = LOG_PATTERN.match(line.rstrip("\n"))
            if match and match.group("level") == "ERROR":
                errors.append((match.group("time"), match.group("message")))
    return errors


def print_table(rows):
    time_width = max([len("시각")] + [len(t) for t, _ in rows])
    msg_width = max([len("메시지")] + [len(m) for _, m in rows])

    header = f"{'시각':<{time_width}} | {'메시지':<{msg_width}}"
    print(header)
    print("-" * len(header))
    for time, message in rows:
        print(f"{time:<{time_width}} | {message:<{msg_width}}")


if __name__ == "__main__":
    errors = parse_errors("sample.log")
    print_table(errors)
