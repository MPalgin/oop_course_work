import requests
import time
from tqdm import tqdm


class YandexDiskUploader:

    def __init__(self, ya_token):
        self.ya_token = ya_token
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def create_folder(self, folder_name):
        if requests.get(url=self.url, headers={'Authorization': f'OAuth {self.ya_token}'},
                        params={'path': folder_name}).status_code != 200:
            requests.put(url=self.url, headers={'Authorization': f'OAuth {self.ya_token}'},
                         params={'path': folder_name}).json()
            for _ in tqdm(range(1, 3), desc='Creating remote folder'):
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
