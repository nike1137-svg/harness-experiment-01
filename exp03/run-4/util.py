from typing import Any


def parse_duration(text: str) -> float:
    """'10s'/'5m'/'2h' 형식의 문자열을 초 단위 float로 변환한다."""
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
    """items를 size 길이의 부분 리스트들로 나눈다."""
    result = []
    for i in range(0, len(items), size):
        result.append(items[i:i + size])
    return result


def safe_get(mapping: dict[str, Any], key: str, default: Any = None) -> Any:
    """'a.b.c' 형식의 점 구분 키로 중첩 dict 값을 조회하고, 없으면 default를 반환한다."""
    parts = key.split(".")
    current = mapping
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
