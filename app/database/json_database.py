import os
import json
from typing import Optional


class JSONDatabase:
    def __init__(self):
        pass

    @staticmethod
    def save_data(data: list) -> None:
        # Check if the file exists and read existing data
        if os.path.exists('db.json'):
            with open('db.json', 'r') as db_file:
                existing_data = json.load(db_file)
        else:
            existing_data = []

        for obj in data:
            existing_data.append(obj)

        # Write the updated data back to the file
        with open('db.json', 'w') as db_file:
            json.dump(existing_data, db_file, indent=4)

    @staticmethod
    def get_data(key: str) -> Optional[list]:
        with open('db.json', 'r') as db_file:
            for line in db_file:
                entry = json.loads(line)
                if entry['url'] == key:  # Adjust condition based on data structure
                    return entry

        return None
