reqistry = {}


def get(name):
    return reqistry[name]


def set(name, value):
    reqistry[name] = value
