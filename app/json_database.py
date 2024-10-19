import json


class JSONDatabase:
    def __init__(self):
        pass

    def save_data(data):
        with open('db.json', 'a') as db_file:
            json.dump(data, db_file)
            db_file.write('\n')  # Write each entry on a new line

    def get_data(key):
        with open('db.json', 'r') as db_file:
            for line in db_file:
                entry = json.loads(line)
                if entry['url'] == key:  # Adjust condition based on data structure
                    return entry
