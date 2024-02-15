import random
import string

from .constants import SHORT_RANDOM_URL


def get_unique_short_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(SHORT_RANDOM_URL))
