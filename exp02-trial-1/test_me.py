# ---- 구현부 (이 부분을 수정하시오) ----------------------------------


def median(numbers):
    ordered = sorted(numbers)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 0:
        return (ordered[middle - 1] + ordered[middle]) / 2
    return ordered[middle]


def percent_change(old, new):
    return (new - old) / old * 100


def flatten(nested):
    out = []
    for item in nested:
        if isinstance(item, list):
            out.extend(item)
        else:
            out.append(item)
    return out


# ---- 테스트부 (수정하지 마시오) --------------------------------------


def test_median_odd():
    assert median([3, 1, 2]) == 2


def test_median_even():
    assert median([4, 1, 3, 2]) == 2.5


def test_percent_change():
    assert percent_change(200, 250) == 25.0


def test_flatten():
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]
