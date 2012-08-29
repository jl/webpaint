"""Small util library demonstrating use of python module import system."""
import random


ALPHANUM = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def random_alphanum(count):
    """Returns a random alphanumeric string."""
    return ''.join((random.choice(ALPHANUM) for i in xrange(count)))
