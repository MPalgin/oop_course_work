import json
from tqdm import tqdm


class JsonCreator:
    def __init__(self, photos_data):
        self.photos_data = photos_data

    def create_json_file(self):
        for _ in tqdm(range(0,6), desc='Creating Json file'):
            with open('recorded_photos_info.json', 'w') as json_file:
                json.dump(self.photos_data, json_file, indent=4)
