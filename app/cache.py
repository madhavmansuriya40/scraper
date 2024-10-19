import json
import os


class Cache:
    def __init__(self, cache_file='cache.json'):
        self.cache_file = cache_file
        self.cache_data = self.load_cache()

    def load_cache(self):
        """Load cache data from a JSON file."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def save_cache(self):
        """Save cache data to a JSON file."""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache_data, f)

    def get(self, key):
        """Retrieve cached data for a specific key."""
        return self.cache_data.get(key)

    def set(self, key, value):
        """Set cached data for a specific key."""
        self.cache_data[key] = value
        self.save_cache()
