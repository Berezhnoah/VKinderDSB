# импорты
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import community_token, access_token
from core import VkTools

class BotInterface():

    def __init__(self,community_token, access_token):
        self.interface = vk_api.VkApi(token=community_token)
        self.api = VkTools(access_token)
        self.params = None
        


    def message_send(self, user_id, message, attachment=None):
        self.interface.method('messages.send',
                                {'user_id': user_id,
                                'message': message,
                                'attachment': attachment,
                                'random_id': get_random_id()
                                }
                                )
        
    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'Приветствую Вас, {self.params["name"]}!')
                elif command == 'поиск':
                    self.message_send (
                        event.user_id, 'Выполняю поиск'
                    )
                    users = self.api.search_users(self.params)
                    user = users.pop()

                    photos_user = self.api.get_photos(user['id'])                  
                    
                    attachment = ''
                    for num, photo in enumerate(photos_user):
                        attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
                        if num == 2:
                            break
                    self.message_send(event.user_id,
                                      f'Знакомьтесь, {user["name"]}! Перейти на страницу: vk.com/{user["id"]}',
                                      attachment=attachment
                                      ) 
                #Альтернативный вариант запроса дополнительных фотографий
                #elif command == 'еще фото':
                    #self.message_send (event.user_id, attachment=attachment)    
                elif command == 'пока':
                    self.message_send(event.user_id, 'До свидания!')
                else:
                    self.message_send(event.user_id, 'Неизвестный запрос')



if __name__ == '__main__':
    bot = BotInterface(community_token, access_token)
    bot.event_handler()