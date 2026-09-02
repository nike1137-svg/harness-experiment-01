def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        return None
    return a / b


def average(nums):
    if not nums:
        return 0
    return sum(nums) / len(nums)
