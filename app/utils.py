import itertools
import random
import string

from app.settings import settings


def generate_prefix() -> str:
    letters = list(string.ascii_lowercase) + list(string.digits)
    combinations = list(itertools.combinations(letters, settings.SHRINK_LENGTH))
    target = random.choice(combinations)

    return "".join(target)
