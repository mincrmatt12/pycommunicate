import random
import string


def random_alphanumeric_string(length):
    chars = list(string.ascii_letters + string.digits + "-_?!., ")
    strin = ""
    for i in range(length):
        strin += random.choice(chars)
    return strin