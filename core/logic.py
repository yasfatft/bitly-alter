import string
import random
import bcrypt
from typing import List
from werkzeug.routing import BaseConverter

from core.models import Url
from core.config import SHORT_URL_LENGTH


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def generate_unique_short_url(long_url: str) -> str:
    short_url = generate_random_string()
    existence = short_url_existence_check(short_url)
    if existence:
        return generate_unique_short_url(long_url)
    return short_url


def generate_random_string():
    letters = string.ascii_lowercase + string.digits
    result = ''.join(random.choice(letters) for i in range(SHORT_URL_LENGTH))
    return result


def short_url_existence_check(short_url: str) -> bool:
    same_short_urls = Url.query.filter_by(short_url=short_url).all()
    return same_short_urls.__len__() > 0


def find_url_with_long_url_and_owner(long_url: str, owner_id: int) ->[bool,
                                                                      List]:
    urls = Url.query.filter_by(long_url=long_url, owner_id=owner_id).all()
    return urls.__len__() > 0, urls

def get_long_url(redis, short_url: str) -> str:
    return redis.get(short_url)[1]


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                    bcrypt.gensalt())
    return hashed_password


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
