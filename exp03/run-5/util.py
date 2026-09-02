def parse_duration(text: str) -> float:
    """'1s', '10m', '2h'처럼 단위가 붙은 문자열을 초 단위 float로 변환한다."""
    unit = text[-1]
    value = float(text[:-1])
    if unit == "s":
        return value
    if unit == "m":
        return value * 60
    if unit == "h":
        return value * 3600
    raise ValueError("unknown unit: " + unit)


def chunk_list[T](items: list[T], size: int) -> list[list[T]]:
    """items를 size 길이씩 잘라 리스트의 리스트로 반환한다."""
    result = []
    for i in range(0, len(items), size):
        result.append(items[i:i + size])
    return result


def safe_get(mapping: dict, key: str, default=None):
    """'a.b.c' 형태의 점 표기 key로 중첩 dict를 탐색하고, 경로가 없으면 default를 반환한다."""
    parts = key.split(".")
    current = mapping
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
