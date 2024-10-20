from pymemcache.client import base


class MemcachedCache:
    def __init__(self) -> None:
        self.client = base.Client(('memcached', '11211'))

    def set(self, key: str, value: str, expire: int = 3600) -> None:
        self.client.set(key, value, expire=expire)

    def get(self, key: str) -> 'MemcachedCache':
        return self.client.get(key)
