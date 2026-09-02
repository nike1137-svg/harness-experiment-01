#!/usr/bin/env python3
"""sample.log에서 ERROR 로그만 뽑아 표로 출력한다."""

import re

LOG_FILE = "sample.log"

# 두 가지 타임스탬프 형식을 모두 지원한다.
#   1) 2026-08-28 09:14:02          (표준 형식)
#   2) 28/Aug/2026:09:18:22         (Apache 스타일)
TIMESTAMP = r"(?:\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}|\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2})"

# 줄 맨 앞의 "레벨" 필드만 검사한다.
# (메시지 본문에 우연히 "ERROR" 단어가 들어간 INFO 줄을 오탐하지 않기 위함)
LINE_RE = re.compile(
    rf"^(?P<ts>{TIMESTAMP})\s+(?P<level>ERROR|WARN|INFO)\s+\[(?P<module>[^\]]+)\]\s+(?P<msg>.*)$"
)

DETAIL_MAX_LEN = 50


def truncate(text, max_len):
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def parse_errors(path):
    errors = []
    current = None  # 마지막으로 발견된 ERROR 레코드 (연속된 상세 줄을 붙이기 위함)

    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            match = LINE_RE.match(line)

            if match:
                if match.group("level") == "ERROR":
                    current = {
                        "ts": match.group("ts"),
                        "module": match.group("module"),
                        "msg": match.group("msg"),
                        "detail": [],
                    }
                    errors.append(current)
                else:
                    current = None  # ERROR가 아닌 새 줄이 나오면 상세 수집 중단
            elif current is not None and line.strip():
                # 들여쓰기된 트레이스백 등 ERROR 줄에 딸린 상세 내용
                current["detail"].append(line.strip())

    return errors


def print_table(errors):
    if not errors:
        print("ERROR 로그가 없습니다.")
        return

    headers = ["시간", "모듈", "메시지", "상세"]
    rows = []
    for e in errors:
        detail = e["detail"][-1] if e["detail"] else "-"
        rows.append(
            [e["ts"], e["module"], e["msg"], truncate(detail, DETAIL_MAX_LEN)]
        )

    widths = [
        max(len(headers[i]), max(len(row[i]) for row in rows))
        for i in range(len(headers))
    ]

    def format_row(cells):
        return " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells))

    separator = "-+-".join("-" * w for w in widths)

    print(format_row(headers))
    print(separator)
    for row in rows:
        print(format_row(row))

    print(f"\n총 ERROR 건수: {len(errors)}")


if __name__ == "__main__":
    errors = parse_errors(LOG_FILE)
    print_table(errors)
