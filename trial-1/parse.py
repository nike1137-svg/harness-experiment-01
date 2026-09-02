#!/usr/bin/env python3
"""sample.log 파일에서 ERROR 줄만 골라 시각과 메시지를 표로 출력한다."""
import re
import sys

LOG_PATTERN = re.compile(r'^(\S+\s+\S+)\s+ERROR\s+(.*)$')


def parse_log(path):
    rows = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            match = LOG_PATTERN.match(line.rstrip('\n'))
            if match:
                rows.append((match.group(1), match.group(2)))
    return rows


def print_table(rows):
    if not rows:
        print("ERROR 줄이 없습니다.")
        return

    time_width = max(len('시각'), max(len(t) for t, _ in rows))
    msg_width = max(len('메시지'), max(len(m) for _, m in rows))

    header = f"{'시각':<{time_width}}  {'메시지':<{msg_width}}"
    print(header)
    print('-' * len(header))
    for t, m in rows:
        print(f"{t:<{time_width}}  {m:<{msg_width}}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'sample.log'
    rows = parse_log(path)
    print_table(rows)


if __name__ == '__main__':
    main()
