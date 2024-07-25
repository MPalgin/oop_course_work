import requests
import time
from tqdm import tqdm
from json_creator import JsonCreator


class VkPhotoDownloader:
    def __init__(self, token, user_id):
        self.user_id = user_id
        self.token = token

    def get_all_photos(self):
        url = 'https://api.vk.com/method/photos.get'

        request_params = {'access_token': self.token, 'owner_id': self.user_id, 'album_id': 'profile',
                          'extended': 1, 'photo_sizes ': 1, 'v': 5.199}
        response = requests.get(url=url, params=request_params).json()
        return response

    def get_photos_data(self, number_of_photos=5):
        photos = self.get_all_photos()
        photos_names = {}
        photos_sizes = []
        index, width, height = 0, 0, 0
        url = ''

        for photos_info in tqdm(photos['response']['items'], desc='Finding photos'):
            if index <= number_of_photos:
                for sizes in photos_info['sizes']:
                    if sizes['width'] > width and sizes['height'] > height:
                        width = sizes['width']
                        height = sizes['height']
                        url = sizes['url']
                if f'{photos_info["likes"]["count"]}.jpg' in photos_names:
                    photos_names[f'{photos_info["likes"]["count"]}_{photos_info["date"]}.jpg'] = url
                else:
                    photos_names[f'{photos_info["likes"]["count"]}.jpg'] = url
                photos_sizes.append({'file_name': f'{photos_info["likes"]["count"]}.jpg',
                                     'height': height, 'width': width})
                time.sleep(1)
                index += 1
                width, height = 0, 0
                url = ''
            else:
                break

        JsonCreator(photos_sizes).create_json_file()

        return photos_names
