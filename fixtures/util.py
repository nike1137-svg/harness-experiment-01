def parse_duration(text):
    unit = text[-1]
    value = float(text[:-1])
    if unit == "s":
        return value
    if unit == "m":
        return value * 60
    if unit == "h":
        return value * 3600
    raise ValueError("unknown unit: " + unit)


def chunk_list(items, size):
    result = []
    for i in range(0, len(items), size):
        result.append(items[i:i + size])
    return result


def safe_get(mapping, key, default=None):
    parts = key.split(".")
    current = mapping
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
