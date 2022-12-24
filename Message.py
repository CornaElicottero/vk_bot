import vk_api
from vk_api.longpoll import VkLongPoll

vk_session = vk_api.VkApi(token='your_token')
longpoll = VkLongPoll(vk_session)
vk_api = vk_session.get_api()
while True:
    A = input()
    F = open('bd.txt', 'r')
    a = F.readlines()
    F.close()
    for i in a:
        s = i[:(len(i) - 1)]
        vk_api.messages.send(user_id=s, message=A, random_id=0)
