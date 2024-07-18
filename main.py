import json

import requests
import time
from tqdm import tqdm

access_token = ''
yandex_token = ''
vk_user_id = '102886405'
number_of_photos = 5


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

    def get_photos_data(self, nums_of_photos=5):
        photos = self.get_all_photos()
        photos_names = {}
        photos_sizes = []
        index = 0
        for photos_info in tqdm(photos['response']['items'], desc='Finding photos'):
            if index <= nums_of_photos:
                for sizes in photos_info['sizes']:
                    if sizes['type'] == 'w':
                        photos_names[f'{photos_info["likes"]["count"]}.jpg'] = sizes['url']
                        photos_sizes.append({'file_name': f'{photos_info["likes"]["count"]}.jpg',
                                             'height': sizes['height'], 'width': sizes['width']})
                time.sleep(1)
                index += 1
            else:
                break

        with open('recorded_photos_info.json', 'w') as json_file:
            json.dump(photos_sizes, json_file, indent=4)

        return photos_names


class YandexDiskUploader:

    def __init__(self, ya_token):
        self.ya_token = ya_token
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def create_folder(self, folder_name):
        if requests.get(url=self.url, headers={'Authorization': f'OAuth {self.ya_token}'},
                        params={'path': folder_name}).status_code != 200:
            requests.put(url=self.url, headers={'Authorization': f'OAuth {self.ya_token}'},
                         params={'path': folder_name}).json()
            for _ in tqdm(range(1,3), desc='Creating remote folder'):
                time.sleep(1)
        else:
            requests.delete(url=self.url, headers={'Authorization': f'OAuth {self.ya_token}'},
                            params={'path': folder_name})
            for _ in tqdm(range(1, 3), desc='Creating remote folder'):
                time.sleep(1)
            requests.put(url=self.url, headers={'Authorization': f'OAuth {self.ya_token}'},
                         params={'path': folder_name})

    def upload_files_to_yandex_disk(self, photos_url, folder_name='vk_photos'):
        self.create_folder(folder_name)

        for file_name in tqdm(photos_url, desc='Uploading photos to Yandex disk'):
            requests.post(url=f'{self.url}upload', headers={'Authorization': f'OAuth {self.ya_token}'},
                          params={'path': f'{folder_name}/{file_name}', 'url': photos_url[file_name]})
            time.sleep(1)
        return 'Photos were uploaded to Yandex Disk'


photos_download = VkPhotoDownloader(access_token, vk_user_id)
photos_upload = YandexDiskUploader(yandex_token)

print(photos_upload.upload_files_to_yandex_disk(photos_download.get_photos_data(number_of_photos)))
