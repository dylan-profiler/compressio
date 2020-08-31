import functools


def compose(functions):
    """
    Compose a sequence of functions
    https://mathieularose.com/function-composition-in-python/

    :param functions: sequence of functions
    :return: combined functions, e.g. [f(x), g(x)] -> f(g(x))
    """

    def compose2(f, g):
        return lambda x: f(g(x))

    return functools.reduce(compose2, functions, lambda x: x)
