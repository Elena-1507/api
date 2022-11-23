import requests
from pprint import pprint
import mytoken



TOKEN_VK = mytoken.vktoken
TOKEN_YANDEX = mytoken.yatoken
URL_VK = 'https://api.vk.com/method/photos.get'

print(TOKEN_VK)
print(TOKEN_YANDEX)


class UserVk:
    
    def __init__(self):
        self.token = TOKEN_VK
        self.version = '5.131'
        

    def get_photo(self, user_id):
        data = requests.get(URL_VK, params={'access_token': TOKEN_VK,
                                            'owner_id': user_id,
                                            'album_id': 'profile',
                                            'extended': '1',
                                            'rev': '1',
                                            'count': '5',
                                            'v': '5.131'}).json()['response']['items']
        dict = {}
        for file in data:
            file_name = file['likes']['count']
            # pprint(file_name)
            photo_url = file['sizes'][-1]['url']
            # dict[file_name] = ['URL:']
            dict[file_name] = [photo_url]
            # pprint(photo_url)
            photo_size = file['sizes'][-1]['type']
            # dict[file_name] = [f'URL: {photo_url}, size: {photo_size}']
            # list.append(f'URL: {photo_url}, name: {file_name}.jpg, size: {photo_size}')

        pprint(dict)
        return dict


class UserYandex:

    def __init__(self):
        self.token = TOKEN_YANDEX
        # self.__headers
    
    def greate_folder(self, name_folder):
        URL = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'OAuth {TOKEN_YANDEX}'}
        requests.put(f'{URL}?path={name_folder}', headers=headers)

    def get_photos_method_url(self, name_folder):
        URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'OAuth {TOKEN_YANDEX}'}
        get_url = requests.get(f'{URL}?path={name_folder}', headers=headers)
        print(get_url)
        return get_url


    def upload_photo(self, name_folder, file_name, photo_url):
        URL = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': f'OAuth {TOKEN_YANDEX}'}
        params = f'{name_folder}/{file_name}'
                   
        res = requests.post(f'{URL}/upload?path={params}&url={photo_url}', headers=headers).json()
        



def main():
    user_id = input('Введите id пользователя Вконтакте: ')
    user_vk = UserVk()
    name_folder = input('Введите название папки: ')
    json_photo = user_vk.get_photo(user_id)
    user_yandex = UserYandex()
    # 
    user_yandex.get_photos_method_url(name_folder)
    user_yandex.greate_folder(name_folder)
    for key, photo in json_photo.items():
        print(key)
        print(photo[0])
        user_yandex.upload_photo(name_folder, f'{key}.jpg', photo[0])
      

if __name__ == '__main__':
    main()
