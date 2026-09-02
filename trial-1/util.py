from typing import Any, Dict, List


def slugify(text: str) -> str:
    """문자열을 소문자 하이픈 슬러그로 변환한다."""
    return text.strip().lower().replace(" ", "-")


def chunk(items: List[Any], size: int) -> List[List[Any]]:
    """리스트를 size 크기의 부분 리스트들로 나눈다."""
    return [items[i:i + size] for i in range(0, len(items), size)]


def merge_defaults(base: Dict[Any, Any], override: Dict[Any, Any]) -> Dict[Any, Any]:
    """base를 override로 덮어쓴 새 딕셔너리를 반환한다."""
    out = dict(base)
    out.update(override)
    return out
