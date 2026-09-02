from typing import Any, Dict, List


def parse_duration(text: str) -> float:
    """단위가 붙은 시간 문자열을 초 단위 실수로 변환한다.

    Args:
        text: 마지막 글자가 단위(s/m/h)인 시간 문자열. 예: "90s", "5m", "2h"

    Returns:
        초 단위로 환산한 값.
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


def chunk_list(items: List[Any], size: int) -> List[List[Any]]:
    """리스트를 지정한 크기의 하위 리스트들로 나눈다.

    Args:
        items: 나눌 원본 리스트.
        size: 하위 리스트 하나의 최대 크기.

    Returns:
        원본 리스트를 size 단위로 나눈 중첩 리스트.
    """
    result = []
    for i in range(0, len(items), size):
        result.append(items[i:i + size])
    return result


def safe_get(mapping: Dict[str, Any], key: str, default: Any = None) -> Any:
    """점(.)으로 구분된 키 경로를 따라 중첩 딕셔너리 값을 안전하게 조회한다.

    Args:
        mapping: 조회할 중첩 딕셔너리.
        key: "a.b.c" 형태의 점 구분 키 경로.
        default: 경로가 존재하지 않을 때 반환할 값.

    Returns:
        경로가 존재하면 해당 값, 없으면 default.
    """
    parts = key.split(".")
    current = mapping
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
