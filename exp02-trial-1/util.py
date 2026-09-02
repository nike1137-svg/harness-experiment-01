from typing import Any, Dict, List, Optional


def parse_duration(text: str) -> float:
    """Parse a duration string like "10s", "5m", "2h" into seconds.

    Args:
        text: Duration string ending in a unit suffix ("s", "m", or "h").

    Returns:
        The duration in seconds.

    Raises:
        ValueError: If the unit suffix is not "s", "m", or "h".
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
    """Split a list into consecutive chunks of at most `size` elements.

    Args:
        items: The list to split.
        size: Maximum number of elements per chunk.

    Returns:
        A list of chunks, each a sublist of `items`.
    """
    result = []
    for i in range(0, len(items), size):
        result.append(items[i:i + size])
    return result


def safe_get(mapping: Dict[str, Any], key: str, default: Optional[Any] = None) -> Any:
    """Look up a dotted key path in a nested dict without raising on misses.

    Args:
        mapping: The (possibly nested) dict to search.
        key: Dot-separated key path, e.g. "a.b.c".
        default: Value to return if any part of the path is missing.

    Returns:
        The value at the key path, or `default` if not found.
    """
    parts = key.split(".")
    current = mapping
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
