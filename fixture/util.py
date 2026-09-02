def slugify(text):
    return text.strip().lower().replace(" ", "-")


def chunk(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]


def merge_defaults(base, override):
    out = dict(base)
    out.update(override)
    return out
