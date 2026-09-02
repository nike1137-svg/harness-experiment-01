from typing import Any, Dict, List


def slugify(text: str) -> str:
    """공백을 하이픈으로 바꾼 소문자 슬러그를 반환한다."""
    return text.strip().lower().replace(" ", "-")


def chunk(items: List[Any], size: int) -> List[List[Any]]:
    """items를 size 크기의 리스트들로 나눈다."""
    return [items[i:i + size] for i in range(0, len(items), size)]


def merge_defaults(base: Dict[Any, Any], override: Dict[Any, Any]) -> Dict[Any, Any]:
    """base에 override를 덮어씌운 새 딕셔너리를 반환한다."""
    out = dict(base)
    out.update(override)
    return out
