import requests
import configparser
from vk_downloader import VkPhotoDownloader
from yandex_uploader import YandexDiskUploader


def get_task_params():
    vk_user_id = input('Введите имя или id профиля: ')
    config = configparser.ConfigParser()
    config.read('config.ini')
    access_token = config['VK']['access_token']
    yandex_token = config['Yandex']['yandex_token']
    number_of_photos = 5

    if config['Num_of_photos']['number_of_photos'] != '':
        number_of_photos = config['Num_of_photos']['number_of_photos']

    if not vk_user_id.isnumeric():

        user_id = requests.get(url='https://api.vk.com/method/users.get',
                               params={'access_token': access_token,
                                       'user_ids': vk_user_id, 'v': 5.199}).json()
        vk_user_id = user_id['response'][0]['id']

    return vk_user_id, access_token, yandex_token, number_of_photos


if __name__ == '__main__':
    vk_user_id, access_token, yandex_token, number_of_photos = get_task_params()

    photos_download = VkPhotoDownloader(access_token, vk_user_id)
    photos_upload = YandexDiskUploader(yandex_token)

    print(photos_upload.upload_files_to_yandex_disk(photos_download.get_photos_data(number_of_photos)))
