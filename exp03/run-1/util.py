from typing import Any


def parse_duration(text: str) -> float:
    """시간 단위 문자열을 초 단위 숫자로 변환한다.

    Args:
        text: 마지막 글자가 단위(s/m/h)인 문자열. 예: "90s", "5m", "2h"

    Returns:
        초 단위로 환산된 값.

    Raises:
        ValueError: 단위가 s, m, h 중 하나가 아닌 경우.
    """
    unit = text[-1]
    value = float(text[:-1])
    if unit == "s":
        return value
    if unit == "m":
        return value * 60
    if unit == "h":
        return value * 3600
    raise ValueError("unknown unit: " + unit)


def chunk_list(items: list[Any], size: int) -> list[list[Any]]:
    """리스트를 지정한 크기 단위로 잘라 리스트의 리스트로 반환한다.

    Args:
        items: 나눌 원본 리스트.
        size: 한 묶음의 최대 크기.

    Returns:
        size 크기로 나뉜 하위 리스트들의 리스트.
    """
    result = []
    for i in range(0, len(items), size):
        result.append(items[i:i + size])
    return result


def safe_get(mapping: dict[str, Any], key: str, default: Any = None) -> Any:
    """점(.)으로 구분된 키 경로를 따라 중첩 딕셔너리 값을 안전하게 조회한다.

    Args:
        mapping: 조회 대상 딕셔너리.
        key: "a.b.c" 형태의 점(.) 구분 키 경로.
        default: 경로 중간에 키가 없거나 dict가 아니면 반환할 기본값.

    Returns:
        경로를 따라 찾은 값, 없으면 default.
    """
    parts = key.split(".")
    current = mapping
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
