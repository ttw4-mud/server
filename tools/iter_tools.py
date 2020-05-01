############################################################

import itertools

############################################################


def list_join(*iters):

    return list(itertools.chain(*iters))


def tuple_join(*iters):

    return tuple(itertools.chain(*iters))


def list_of_keys(some_dict):

    return list(some_dict.keys())
