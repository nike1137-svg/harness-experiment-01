from calc import add, divide, average


def test_add():
    assert add(2, 3) == 5


def test_divide_ok():
    assert divide(6, 3) == 2


def test_divide_by_zero():
    assert divide(1, 0) is None


def test_average_ok():
    assert average([1, 2, 3]) == 2


def test_average_empty():
    assert average([]) == 0
