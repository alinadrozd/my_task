import requests
from pprint import pprint
import time
import yadisk
import os
from progress.bar import IncrementalBar

with open('my_token.md') as file_1:
    TOKEN_VK = file_1.readline().strip()
    TOKEN_YA = file_1.readline().strip()


class UserVk:
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_photo(self, user_id, extending=1, photos_sizes=1):
        url_1 = 'https://api.vk.com/method/photos.get'
        params = {'access_token': TOKEN_VK,
                  'v': '5.131',
                  'album_id': 'profile',
                  'extending': 1,
                  'count': 5}
        req = requests.get('https://api.vk.com/method/photos.get', params)
        if req.status_code == 200:
            pprint(req)
            req = req.json()['response']['items']
            return req
        else:
            print('Ошибка получения фото')
            return None

    def parsed_photo(self, photos_info: list):
        photo_list = ['']
        photo_sizes = 1
        url_1 = 'https://api.vk.com/method/photos.get'
        params = {'access_token': TOKEN_VK,
                  'v': '5.131',
                  'album_id': 'profile',
                  'extending': 1,
                  'count': 5}
        req = requests.get('https://api.vk.com/method/photos.get', params)
        imageLink = user[0]['photo_max_orig']
        height = 0
        count = 5
        for i in range(0, len(photo_dict)):
            for photo in photo_list[i]:
                    for size in photo['sizes']:
                        if size['height'] > height:
                            height = size['height']
      
                    data = {'date': photo['date'], 'long': photo['long']}
                    photo_list.append(data)

        return photo_list
        print (photo_list)


class YandexUpload:
    URL_FILES_LIST: str = 'https://cloud-api.yandex.net/v1/disk/resoures/files'
    URL_UPLOAD_LINK: str = 'https://cloud-api.yandex.net/v1/disk/resoures/upload'

    def __init__(self, token: str):
        self.header = None
        self.token = token

    def upload(self, file_path: str):
        return {"Content-Type": "application/json", "authorization": f"QAuth {self.token}"}

    def get_files_list(self):
        response = requests.get(self.URL_FILES_LIST)
        return response.json()

    def get_upload_link(self, ya_disk_path: str):
        params = {"path": ya_disk_path, "overwrite": "true"}
        response = requests.get(self.URL_UPLOAD_LINK, headers=self.header, params=params)
        upload_url = response.json().get("href")
        ya_disk_path.mkdir("/test/My_folder")
        return upload_url


access_token = TOKEN_VK
user_id = ''
vk = UserVk(access_token, user_id)
print(vk.users_info())


def main():
    user_id = input('Введите id пользователя: ')
    user_vk = UserVk(access_token, user_id)
    name_directory = input('Введите название папки:')
    json_photo = user_vk.get_photo(user_id)
    parsed_photo = user_vk.parsed_photo(json_photo)
    user_yandex = YandexUpload()
    user_yandex.create_folder(name_directory)
    user_yandex.upload_file(parsed_photo, name_directory)

    bar = IncrementalBar('Осталось:', max=len(parsed_photo))


    for photo in parsed_photo:
      bar.next()
      time.sleep(1)
      bar.finish()

if __name__ == '__main__':
    main()
