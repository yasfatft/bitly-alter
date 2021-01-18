import redis

from core.models import Url


class Redis:
    def __init__(self, host, port):
        self._connection = redis.StrictRedis(host=host, port=port)

    def populate_redis(self):
        urls = Url.query.filter().all()
        for url in urls:
            self._connection.set(url.short_url, url.long_url)
        return True

    def add_to_redis(self, key, value):
        return self._connection.set(key, value)

    def get(self, key):
        return True, self._connection.get(key)
