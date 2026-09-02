"""sample.log에서 ERROR 레벨 줄만 골라 표로 출력하는 스크립트.

로그 한 줄의 기본 형식: "<타임스탬프> <레벨> [<컴포넌트>] <메시지>"
타임스탬프는 두 가지 형식을 지원한다.
  - "2026-08-28 09:14:02" (기본 형식)
  - "28/Aug/2026:09:18:22" (Apache 스타일)

주의사항:
  - Traceback처럼 위 형식에 맞지 않는 줄(들여쓰기된 부가 정보)은 무시한다.
  - 레벨이 INFO/WARN인데 메시지 안에 "ERROR"라는 단어가 들어있는 경우는
    오류로 취급하지 않는다 (레벨 필드만 기준으로 판단).
"""

import re
import sys

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    r"|\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})"
    r"\s+(?P<level>ERROR|WARN|INFO)"
    r"\s+\[(?P<component>[^\]]+)\]"
    r"\s+(?P<message>.*)$"
)


def parse_errors(path: str) -> list[dict[str, str]]:
    """로그 파일을 읽어 ERROR 레벨 줄만 파싱해 반환한다.

    Args:
        path: 읽을 로그 파일 경로.

    Returns:
        각 ERROR 줄을 timestamp/component/message 키로 담은 딕셔너리 리스트.
    """
    errors = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            match = LOG_PATTERN.match(line.rstrip("\n"))
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


def print_table(rows: list[dict[str, str]]) -> None:
    """ERROR 목록을 표 형태로 출력한다.

    Args:
        rows: parse_errors가 반환한 딕셔너리 리스트.
    """
    headers = ("시각", "컴포넌트", "메시지")
    keys = ("timestamp", "component", "message")
    widths = [
        max(len(h), *(len(r[k]) for r in rows)) if rows else len(h)
        for h, k in zip(headers, keys)
    ]

    def fmt_row(values: tuple[str, str, str]) -> str:
        return " | ".join(v.ljust(w) for v, w in zip(values, widths))

    print(fmt_row(headers))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(fmt_row((r["timestamp"], r["component"], r["message"])))


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "sample.log"
    errors = parse_errors(path)
    if not errors:
        print(f"{path}에서 ERROR 줄을 찾지 못했습니다.")
        return
    print_table(errors)
    print(f"\n총 {len(errors)}건")


if __name__ == "__main__":
    main()
