import time
from datetime import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import vk_api
from bs4 import BeautifulSoup
from vk_api import VkUpload
import random


def weekday(day):
    if day == 0:
        return 'понедельник'
    if day == 1:
        return 'вторник'
    if day == 2:
        return 'среда'
    if day == 3:
        return 'четверг'
    if day == 4:
        return 'пятница'
    if day == 5:
        return 'суббота'
    if day == 6:
        return 'воскресенье'


'''def get_weather_today() -> list:
    http = "https://sinoptik.com.ru/погода-сургут-101490624"
    b = BeautifulSoup(requests.get(http).text, "html.parser")

    p3 = b.select('.temperature .p3')
    weather1 = p3[0].getText()
    p4 = b.select('.temperature .p4')
    weather2 = p4[0].getText()
    p5 = b.select('.temperature .p5')
    weather3 = p5[0].getText()
    p6 = b.select('.temperature .p6')
    weather4 = p6[0].getText()

    result = ''
    result = result + ('Утром :' + weather1 + ' ' + weather2) + '\n'
    result = result + ('Днём :' + weather3 + ' ' + weather4) + '\n'
    temp = b.select('.rSide .description')
    weather = temp[0].getText()
    result = result + weather.strip()

    return result
'''


def quote():
    http = "https://randstuff.ru/fact/"
    b = BeautifulSoup(requests.get(http).text, "html.parser")
    quote1 = b.find('div', {'id': 'fact'})
    current_quote = quote1.contents[0].getText()
    return current_quote


def joke():
    http = "https://randstuff.ru/joke/"
    b = BeautifulSoup(requests.get(http).text, "html.parser")
    joke1 = b.find('div', {'id': 'joke'})
    current_joke = joke1.contents[0].getText()
    return current_joke


def weatherNow():
    http = "https://yandex.ru/pogoda/surgut"
    b = BeautifulSoup(requests.get(http).text, "html.parser")
    weather1 = b.find('span', {'class': 'temp__value'})
    weather = weather1.contents[0]
    return 'В данный момент в Сургуте: ' + weather + '°'


def lessonEnd():
    if datetime.weekday(datetime.now()) == 6:
        return 'Вы только посмотрите! Оказывается, что в воскресенье нет уроков! Удивительно, не правда ли?'
    a, last = map(int, RTimetable[datetime.weekday(datetime.now())][
        len(LTimetable[datetime.weekday(datetime.now())]) - 1].split())
    now = datetime.strftime(datetime.now(), '%H %M')
    h, m = now.split()
    m = getMinutes(h, m)
    if m < 480:
        return 'Минут до начала урока: ' + str(480 - m)
    elif m > last:
        return 'Сейчас уроков нет'
    for current_lesson in RTimetable[datetime.weekday(datetime.now())]:
        ls, le = map(int, current_lesson.split())
        if ls <= m <= le and m <= last:
            if le - m == 0:
                return 'До конца урока осталось менее минуты'
            else:
                return 'Минут до конца урока: ' + str(le - m)
    for i in range(1, len(RTimetable[datetime.weekday(datetime.now())])):
        ts = int(RTimetable[datetime.weekday(datetime.now())][i - 1][
                 RTimetable[datetime.weekday(datetime.now())][i - 1].find(' ') + 1:])
        te = int(RTimetable[datetime.weekday(datetime.now())][i][
                 :RTimetable[datetime.weekday(datetime.now())][i - 1].find(' ')])
        if ts <= m <= te and m < last:
            return 'Минут до начала урока: ' + str(te - m)


def getMinutes(h, m):
    while h[0] == '0' and len(h) != 1:
        h = h[1:]
    while m[0] == '0' and len(m) != 1:
        m = m[1:]
    return int(h) * 60 + int(m)


def getLesson():
    if datetime.weekday(datetime.now()) == 6:
        return 'Вы только посмотрите! Оказывается, что в воскресенье нет уроков! Удивительно, не правда ли?'
    last = 0
    c = -1
    now = datetime.strftime(datetime.now(), '%H %M')
    h, m = now.split()
    m = getMinutes(h, m)
    for current_lesson in RTimetable[datetime.weekday(datetime.now())]:
        c += 1
        ls, le = map(int, current_lesson.split())
        if c < len(LTimetable[datetime.weekday(datetime.now())]) and last < le:
            last = le
        if ls <= m <= le and c < len(LTimetable[datetime.weekday(datetime.now())]):
            return 'Сейчас ' + str(LTimetable[datetime.weekday(datetime.now())][c])
    if m >= last:
        return 'Сейчас уроков нет'
    c = 0
    for i in range(1, len(RTimetable[datetime.weekday(datetime.now())])):
        c += 1
        ts = int(RTimetable[datetime.weekday(datetime.now())][i - 1][
                 RTimetable[datetime.weekday(datetime.now())][i - 1].find(' ') + 1:])
        te = int(RTimetable[datetime.weekday(datetime.now())][i][
                 :RTimetable[datetime.weekday(datetime.now())][i - 1].find(' ')])
        if ts <= m <= te and c < len(LTimetable[datetime.weekday(datetime.now())]):
            return 'Следующий урок - ' + str(LTimetable[datetime.weekday(datetime.now())][c])
        elif c >= len(LTimetable[datetime.weekday(datetime.now())]):
            return 'Сейчас уроков нет'
        elif m < 480:
            return 'Следующий урок - ' + str(LTimetable[datetime.weekday(datetime.now())][0])
    return 'Сейчас уроков нет'


file = open('alarm_schedule.txt', 'r')
RTimetable = []
RDay = []
c = 0
k = 0
Lstart = Lend = hs = ms = he = me = ''
stroke = 'NotEmpty'
while stroke != '':
    stroke = file.readline()
    stroke = stroke[:len(stroke) - 1]
    while stroke not in '0123456*':
        RDay.append(stroke)
        stroke = file.readline()
        stroke = stroke[:len(stroke) - 1]
    if RDay:
        RTimetable.append(RDay)
    RDay = []
file.close()
for Day in RTimetable:
    for Lesson in Day:
        for symbol in range(len(Lesson)):
            if Lesson[symbol] != ' ':
                Lstart += Lesson[symbol]
            else:
                Lend = Lesson[symbol + 1:len(Lesson)]
                break
        for symbol in range(len(Lstart)):
            if Lstart[symbol] != ':':
                hs += Lstart[symbol]
            else:
                ms = Lstart[symbol + 1:len(Lstart)]
                break
        for symbol in range(len(Lend)):
            if Lend[symbol] != ':':
                he += Lend[symbol]
            else:
                me = Lend[symbol + 1:len(Lend)]
                break
        Day[k] = str(getMinutes(hs, ms)) + ' ' + str(getMinutes(he, me))
        Lstart = Lend = hs = ms = he = me = ''
        k += 1
    k = 0
    RTimetable[c] = Day
    c += 1
file = open('subject_schedule.txt', 'r')
LTimetable = []
LDay = []
c = 0
k = 0
stroke = 'NotEmpty'
while stroke != '':
    stroke = file.readline()
    stroke = stroke[:len(stroke) - 1]
    while stroke not in '012345*':
        LDay.append(stroke)
        stroke = file.readline()
        stroke = stroke[:len(stroke) - 1]
    if LDay:
        LTimetable.append(LDay)
    LDay = []
file.close()
insult_trigger = ["Соси", "Пидор", "Сука", "Гондон", "Имбицил", "Пшлнх", "пшлнх", "ПШЛНХ", "Хуй", "Уебок", "Блять",
                  "Блядь", "Блеадь", "Блеать", "Петух", "Пизда", "Нахуй", "соси", "пидор", "сука", "гондон", "имбицил",
                  "хуй", "уебок", "блять", "блядь", "блеадь", "блеать", "петух", "пизда", "нахуй", "Даун", "даун",
                  "Хуесос", "хуесос", "Лох", "лох", "Гондон", "гондон", "Чмо", "чмо", "Залупа", "залупа"]
insult_bad = ["Сам соси", "Пшлнх", "Пидор", "Мать ебал", "Shut up nigga", "STFU", "Катись отсюда амеба",
              "Мне похуй нахуй", "Ты уверен?", "Ты приёмный", "А может ты саси?", "БАН", "Не, ну это бан"]
insult_good = ["Любое сходство между вами и человеком является чисто случайным!",
               "Вы всегда так глупы, или сегодня особый случай?", "Как аутсайдер, что вы думаете о человеческой расе?",
               "Я хотел бы вам ударить в зубы, но почему я должен улучшать ваш внешний вид?",
               "По крайней мере, есть одна положительная вещь, в вашем теле. Оно не такое страшное, как ваше лицо!",
               "Мозг еще не все. А в вашем случае он ничего!", "Осторожнее, не позволяйте мозгу влезть вам в голову!",
               "Вы мне нравитесь. Говорят, у меня отвратительный вкус, но я вас люблю.",
               "Ваши родители когда-нибудь просили вас убежать из дома?",
               "Продолжайте говорить, когда-нибудь вам все-таки удастся сказать что-нибудь умное!",
               "Вы все еще любите природу, несмотря на то, что она сделала с вами?",
               "Он задумался – это что-то новенькое.", "Когда, наконец, стемнеет, вы наверняка будете выглядеть лучше!",
               "В книге «Кто есть кто» вас следует искать как Что Это?",
               "Вы являетесь живым доказательством того, что человек может жить без мозгов!",
               "Да вы просто шаблон для построения идиота.",
               "Почему ты здесь? Я думал, что зоопарк закрывается на ночь!",
               "Как ты сюда попал? Неужели кто-то оставил клетку открытой?",
               "Не пытайтесь ничего найти у себя в голове, она же пустая.",
               "Я думаю, вы бы не хотели, чувствовать себя так, как вы выглядите!",
               "Я знаю, вы родились глупым, но почему у вас рецидив?",
               "Я знаю, вы не так глупы, как выглядите. Такое невозможно!",
               "Я видел людей, как ты, но тогда я должен был заплатить за билет!"]
F = open('bd.txt')
vk_session = vk_api.VkApi(token='your_token')

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
session = requests.Session()
count = 0
upload = VkUpload(vk_session)
while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                if event.text == 'Привет' or event.text == 'Дарова':
                    if event.from_user:
                        vk.messages.send(
                            user_id=event.user_id,
                            message=str('Здравствуй, ' + vk.users.get(user_id=event.user_id, fields='city')[0][
                                'first_name'] + '!'),
                            random_id=event.random_id,
                            keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                        )
                elif event.text == '!подписка' or event.text == '!Подписка':
                    if event.from_user:
                        F = open('bd.txt', 'r+')
                        if (str(event.user_id) + '\n') in F.readlines():
                            vk.messages.send(
                                user_id=event.user_id,
                                message='Вы и так уже подписаны!',
                                random_id=event.random_id,
                                keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                            )
                            F.close()
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message='Вы были подписаны на рассылку!',
                                random_id=event.random_id,
                                keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                            )
                            F = open('bd.txt', 'a')
                            F.write(str(event.user_id) + '\n')
                            F.close()
                elif event.text == '!отписка' or event.text == '!Отписка':
                    if event.from_user:
                        F = open('bd.txt', 'r')
                        a = F.readlines()
                        if (str(event.user_id) + '\n') in a:
                            vk.messages.send(
                                user_id=event.user_id,
                                message='Вы были отписаны от рассылки!',
                                random_id=event.random_id,
                                keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                            )
                            F.close()
                            F = open('bd.txt', 'w')
                            for line in a:
                                if line != (str(event.user_id) + '\n'):
                                    F.write(line)
                            F.close()
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message='Вы и так не подписаны на рассылку!',
                                random_id=event.random_id,
                                keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                            )
                elif event.text == 'Сколько до звонка?' or event.text == 'сколько до звонка' or event.text == '1':
                    if event.from_user:
                        s = ''
                        for i in lessonEnd():
                            s = s + str(i)
                        vk.messages.send(
                            user_id=event.user_id,
                            message=str(lessonEnd()),
                            random_id=event.random_id,
                            keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                        )
                elif event.text == 'Какой урок?' or event.text == 'какой урок' or event.text == '2':
                    if event.from_user:
                        vk.messages.send(
                            user_id=event.user_id,
                            message=str(getLesson()),
                            random_id=event.random_id,
                            keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                        )
                elif event.text == 'Погода' or event.text == 'погода' or event.text == '3':
                    if event.from_user:
                        vk.messages.send(
                            user_id=event.user_id,
                            message=weatherNow(),
                            random_id=event.random_id,
                            keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                        )
                elif event.text == 'ПогодаСейчас' or event.text == 'погодасейчас':
                    if event.from_user:
                        vk.messages.send(
                            user_id=event.user_id,
                            message=weatherNow(),
                            random_id=event.random_id,
                            keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                        )
                elif event.text == 'Факт' or event.text == 'факт':
                    if event.from_user:
                        vk.messages.send(
                            user_id=event.user_id,
                            message=quote(),
                            random_id=event.random_id,
                            keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                        )
                elif event.text == 'Шутка' or event.text == 'шутка':
                    if event.from_user:
                        vk.messages.send(
                            user_id=event.user_id,
                            message=joke(),
                            random_id=event.random_id,
                            keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                        )
                elif event.text == 'Команды' or event.text == 'команды':
                    if event.from_user:
                        vk.messages.send(
                            user_id=event.user_id,
                            message='Мои команды:\n1)Сколько до звонка?\n2)Какой урок?\n3)Погода\n\nТакже вы можете '
                                    'подписаться на рассылку сообщений написав "!подписка" и отписаться от нее '
                                    'написав "!отписка"',
                            random_id=event.random_id,
                            keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                        )
                elif '!рассылка' in event.text:
                    if event.from_user and event.user_id == 'your_id':
                        F = open('bd.txt', 'r')
                        a = F.readlines()
                        F.close()
                        try:
                            for i in a:
                                s = i[:(len(i) - 1)]
                                vk.messages.send(user_id=s, message=str(event.text[10:]), random_id=0,
                                                 keyboard=open('keyboard.json', 'r', encoding='UTF-8').read())
                        except:
                            vk.messages.send(user_id='your_id', message='Сообщение пустое! Повторите попытку!',
                                             random_id=0)
                elif event.text == '!подпискаМемы' or event.text == '!ПодпискаМемы':
                    if event.from_user:
                        F = open('bd_memes.txt', 'r+')
                        if (str(event.user_id) + '\n') in F.readlines():
                            vk.messages.send(
                                user_id=event.user_id,
                                message='Вы и так уже подписаны на мемы!',
                                random_id=event.random_id
                            )
                            F.close()
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message='Вы были подписаны на рассылку мемов!',
                                random_id=event.random_id
                            )
                            F = open('bd_memes.txt', 'a')
                            F.write(str(event.user_id) + '\n')
                            F.close()
                elif event.text == '!отпискаМемы' or event.text == '!ОтпискаМемы':
                    if event.from_user:
                        F = open('bd_memes.txt', 'r')
                        a = F.readlines()
                        if (str(event.user_id) + '\n') in a:
                            vk.messages.send(
                                user_id=event.user_id,
                                message='Вы были отписаны от рассылки мемов!',
                                random_id=event.random_id
                            )
                            F.close()
                            F = open('bd_memes.txt', 'w')
                            for line in a:
                                if line != (str(event.user_id) + '\n'):
                                    F.write(line)
                            F.close()
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message='Вы и так не подписаны на рассылку мемов!',
                                random_id=event.random_id
                            )
                elif '!Мемы' in event.text:
                    attachments = []
                    if event.from_user and event.user_id == 'your_id':
                        F = open('bd_memes.txt', 'r')
                        a = F.readlines()
                        F.close()
                        image_url = str(event.text[5:])
                        image = session.get(image_url, stream=True)
                        photo = upload.photo_messages(photos=image.raw)[0]
                        attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
                        try:
                            for i in a:
                                s = i[:(len(i) - 1)]
                                vk.messages.send(user_id=s, message='Вот ваш мем!', attachment=','.join(attachments),
                                                 random_id=0)
                        except:
                            vk.messages.send(user_id='your_id', message='Сообщение пустое! Повторите попытку!',
                                             random_id=0)
                elif event.from_user:
                    for i in insult_trigger:
                        if i in event.text:
                            count += 1
                    if count > 0:
                        vk.messages.send(user_id=event.user_id,
                                         message=insult_good[random.randint(0, (len(insult_good) - 1))],
                                         random_id=event.random_id)
                        count = 0
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            message='Не понял тебя! Пиши "Команды"!',
                            random_id=event.random_id,
                            keyboard=open('keyboard.json', 'r', encoding='UTF-8').read()
                        )

    except Exception as e:
        vk.messages.send(user_id='your_id', message=str(e), random_id=0)
        time.sleep(300)
        continue
