import vk_api
from vk_api.longpoll import VkLongPoll

vk_session = vk_api.VkApi(token='6691eb9b8d09d68cc022c09dbc9de5bf06c11834610b1af00117c683fb5311dd66cdcb10015e9135d366b')
longpoll = VkLongPoll(vk_session)
vk_api = vk_session.get_api()
while True:
    A = input()
    F = open('BD.txt', 'r')
    a = F.readlines()
    F.close()
    for i in a:
        s = i[:(len(i) - 1)]
        vk_api.messages.send(user_id=s, message=A, random_id=0)
