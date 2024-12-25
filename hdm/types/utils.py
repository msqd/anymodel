def mapper(mixed):
    return getattr(mixed, "__mapper__", None)


def getmeta(mixed, key, default=None):
    metadata = getattr(mixed, "__metadata__", None)
    if metadata:
        return metadata.get(key, default)
    return default
