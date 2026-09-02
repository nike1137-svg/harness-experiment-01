from typing import Any, List, Optional


def parse_duration(text: str) -> float:
    """단위가 붙은 기간 문자열을 초 단위 숫자로 변환한다.

    Args:
        text: 숫자 뒤에 단위(s, m, h)가 붙은 문자열. 예: "90s", "5m", "2h".

    Returns:
        초 단위로 환산된 값.
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
    """리스트를 지정한 크기 단위로 잘라 중첩 리스트로 반환한다.

    Args:
        items: 나눌 대상 리스트.
        size: 한 묶음의 최대 길이.

    Returns:
        size 길이로 잘린 부분 리스트들을 담은 중첩 리스트.
    """
    result = []
    for i in range(0, len(items), size):
        result.append(items[i:i + size])
    return result


def safe_get(mapping: dict, key: str, default: Optional[Any] = None) -> Any:
    """점(.)으로 구분된 키 경로를 따라 중첩 딕셔너리 값을 안전하게 조회한다.

    Args:
        mapping: 조회 대상 딕셔너리.
        key: "a.b.c"처럼 점으로 구분된 키 경로.
        default: 경로 중간에 값이 없을 때 반환할 기본값.

    Returns:
        경로를 따라 찾은 값. 경로가 존재하지 않으면 default.
    """
    parts = key.split(".")
    current = mapping
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
