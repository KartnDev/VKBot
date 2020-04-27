import asyncio
import threading

from vk_api.longpoll import VkLongPoll, VkEventType
from Database.CommandDbWorker import CommandWorker
from Database.UserDbWorker import UserWorker
from StartupLoader.StartupLoader import StartupLoader
import vk_api
import random
import math
import sched, time

# Предзагрузка конфигураций
config_loader = StartupLoader('config.JSON')

admin_id_int = config_loader.get_admin_id()

# Создание БД воркеров
user_worker = UserWorker()
command_worker = CommandWorker()

# Загрузка листов из БД
commands = command_worker.select_all()
users = user_worker.select_all()

# Инициализация vk_api
vk_session = vk_api.VkApi(token=config_loader.get_vk_token())
session_api = vk_session.get_api()
long_poll = VkLongPoll(vk_session)

# код для работы экспы



dict_of_levels = {
    1: 1000,
    2: 2700,
    3: 8900,
    4: 20000,
    5: 54590,
    6: 148400,
    7: 1000000
}


def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send',
                      {id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648),
                       "attachment": attachment, 'keyboard': keyboard})


"""Возвтращает True если у человека доступ такой же или выше, в иных случаях False"""


def is_permitted(vk_id: int, required_level: int):
    for user in users:
        if user['vk_id'] == int(vk_id):
            return user['access_level'] >= required_level
    return False


def get_pictures(vk_session, id_group, vk):
    try:
        attachment = ''
        max_num = vk.photos.get(owner_id=id_group, album_id='wall', count=0)['count']
        num = random.randint(1, max_num)
        pictures = vk.photos.get(owner_id=str(id_group), album_id='wall', count=1, offset=num)['items']
        buf = []
        for element in pictures:
            buf.append('photo' + str(id_group) + '_' + str(element['id']))
        print(buf)
        attachment = ','.join(buf)
        print(type(attachment))
        print(attachment)
        return attachment
    except:
        return get_pictures(vk_session, id_group, vk)


def distribution_func(value: int):
    if value < 50:
        return 5 * math.sin(2 * math.pi * value - math.pi / 2) + 6.2
    else:
        return 6 / value


async def longpoolHandle():
    user_spam_coeffs = dict(zip([user['vk_id'] for user in users], [1] * len(users)))
    counter_of_messages = 0
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            counter_of_messages += 1
            #TODO REWRITE IT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! (without message or more logics from)
            if counter_of_messages >= 150:
                user_spam_coeffs = dict(zip([user['vk_id'] for user in users], [1] * len(users)))
                counter_of_messages = 0
            response = event.text
            current_user = {'access_level': 0,
                            'vk_id': None,
                            'association': "Unknown",
                            'lvl_exp': 0}
            if event.from_chat:
                for user in users:
                    if user['vk_id'] == int(event.extra_values['from']):
                        current_user = user
                        if user['access_level'] < 8:
                            coef = 2
                            user['lvl_exp'] += distribution_func(len(event.text.split(' '))) / coef * \
                                               user_spam_coeffs[user['vk_id']]
                            if user_spam_coeffs[user['vk_id']] > 0.7:
                                user_spam_coeffs[user['vk_id']] -= 0.03
                            else:
                                user_spam_coeffs[user['vk_id']] *= 0.57
                            print(user_spam_coeffs[user['vk_id']])
                            if user['lvl_exp'] >= dict_of_levels[user['access_level']]:
                                user['lvl_exp'] = 0
                                # level up
                                user['access_level'] += 1
                                send_message(vk_session, 'chat_id', event.chat_id, "@id" + event.extra_values['from']
                                             + "Апнул " + str(user['access_level']) + 'левел!')
                                # TODO bd.update(user['vk_id], user['access_level'])

            for item in commands:
                if item['name'] == event.text:
                    # from chat
                    send_message(vk_session, 'chat_id', event.chat_id, item['value'])

            if event.text == "!камни":
                send_message(vk_session, 'chat_id', event.chat_id,
                             '🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿' +
                             '🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿')
            if event.text == "!vkbot":
                send_message(vk_session, 'chat_id', event.chat_id,
                             'Комманды бота Ильи: \n >>>>>>>>>>>>>>>>>>>> \n <<КОМАНДЫ>> \n  ' +
                             '\n •!шанс ---->узнать шанс чего-либо \n •!шар --->вопрос, после чего будет ' +
                             'выдан ответ \n  \n <<РАНДОМ АНИМЕ АРТЫ>> \n  \n •!лоли \n •!юри \n •!ахегао ' +
                             '\n •!фейт прикол \n •!фейт арт \n •!камшот \n \n <<3Д ТЯНКИ И НЕ ТОЛЬКО>> \n  \n' +
                             ' •!3д мусор \n •!кукла \n \n <<ТОСАКА РИН>> \n \n •!тосака \n •!тосака2 ---> хентай' +
                             ' \n •!иштар \n •!эриш  \n \n <<ПРОЧЕЕ ГОВНО>> \n \n •!камни \n ' +
                             '•!палата шевцова \n •!хуесосина \n •!колда \n •!музыка \n •!радмир \n •!клоун',
                             attachment='photo564230346_457239307')
            if event.text == "!лоли":
                code = [-127518015, -157516431]
                attachment = get_pictures(vk_session, random.choice(code), session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи девочку!', attachment)
            if event.text == "!юри":
                code = [-153284406, -157516431]
                attachment = get_pictures(vk_session, random.choice(code), session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи лесбух!', attachment)
            if event.text == "!ахегао":
                attachment = get_pictures(vk_session, -128535882, session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи ахегао, конченый извращенец!', attachment)
            if event.text == "!палата шевцова":
                attachment = get_pictures(vk_session, -88245281, session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи мем из палаты Шевцова!', attachment)
            if event.text == "!фейт прикол":
                attachment = get_pictures(vk_session, -183563128, session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи мем из группы Fate/GrandПрикол!', attachment)
            if event.text == "!фейт арт":
                attachment = get_pictures(vk_session, -191752227, session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи арт из группы far side of the moon!',
                             attachment)
            if event.text == "!3д мусор":
                attachment = get_pictures(vk_session, -70232735, session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи свой 3д мусор!', attachment)
            if event.text == "!кукла":
                attachment = get_pictures(vk_session, -186765691, session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи свою куклу, куклоёб!', attachment)
            if event.text == "!хуесосина":
                send_message(vk_session, 'chat_id', event.chat_id, attachment='video210923765_456239281')
            if event.text == "!колда":
                send_message(vk_session, 'chat_id', event.chat_id, attachment='video537612639_456239020')
            if event.text == "!музыка":
                send_message(vk_session, 'chat_id', event.chat_id,
                             attachment='audio564230346_456239018,audio564230346_456239019,audio564230346_456239017')
            if event.text == "!тосака":
                attachment = get_pictures(vk_session, -119603422, session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи Тосаку!', attachment)
            if event.text == "!тосака2":
                attachment = get_pictures(vk_session, -119603422, session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи хентайную Тосаку!', attachment)
            if event.text == "!иштар":
                code = [-119603422, -88245281]
                attachment = get_pictures(vk_session, random.choice(code), session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи Иштар!', attachment)
            if event.text == "!эриш":
                attachment = get_pictures(vk_session, -119603422, session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи Эрешкигаль!', attachment)
            if event.text == "!радмир":
                send_message(vk_session, 'chat_id', event.chat_id, attachment='photo564230346_457239374')
            if event.text == "!клоун":
                send_message(vk_session, 'chat_id', event.chat_id, attachment='photo564230346_457239422')

            if event.text == "!камшот":
                attachment = get_pictures(vk_session, -2343758, session_api)
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи рандом скриншот!', attachment)
            if event.text == "!кто":
                if event.from_chat:
                    val = random.choice((vk_session.method('messages.getChat', {'chat_id': event.chat_id}))['users'])
                    send_message(vk_session, 'peer_id', event.peer_id, "@id" + str(val))
            if event.text == "!gvn":
                huy = vk_session.method('video.get', {'owner_id': '-164489758', 'count': 200, 'offset': 1})['items']
                qwert = random.choice(list(i for i in huy))
                send_message(vk_session, 'peer_id', event.peer_id, 'Держи gvn!',
                             attachment='video' + str(-164489758) + '_'
                                        + str(qwert['id']))
            if event.text == '!статус':
                # TODO WTF rewrite it
                found = False
                for user in users:
                    if str(user['vk_id']) == event.extra_values['from']:
                        send_message(vk_session, 'chat_id', event.chat_id, "Вы зарегестрированы как " +
                                     user['association'] + " и ваш текущий уровень: " +
                                     str(user['access_level']) + 'lvl и ' + str(round(user['lvl_exp'], 2)) + 'опыта')
                        found = True
                if not found:
                    send_message(vk_session, 'chat_id', event.chat_id, "Вы не зарегестрированы ;d" +
                                 " чтобы разегаться юзай !regme <ник>")
            spaced_words = str(response).split(' ')

            if spaced_words[0] == '!шанс' and len(spaced_words) > 1:
                send_message(vk_session, 'peer_id', event.peer_id,
                             'Шанс того, что ' + ' '.join(spaced_words[1:]) + ' - '
                             + str(random.randint(1, 100)) + '%')
            if spaced_words[0] == '!шар':
                send_message(vk_session, 'peer_id', event.peer_id, 'Мой ответ - ' +
                             str(random.choice(["Да",
                                                "Нет",
                                                "Скорее всего, но это не точно",
                                                "В душе не ебу если честно",
                                                "Да, это прям 100%",
                                                "нет,ты чё шизоид?"])) + ' ')

            """ Добавление и редактирование в список пользователей """
            if spaced_words[0] == '!regme' and len(spaced_words) == 2:
                if (spaced_words[1] not in list(i['association'] for i in users)) or \
                        (int(event.extra_values['from']) not in list(i['vk_id'] for i in users)):
                    if admin_id_int != int(event.extra_values['from']):
                        user_worker.insert(1, event.extra_values['from'], spaced_words[1])
                        users.insert(0, {
                            'access_level': 1,
                            'vk_id': event.extra_values['from'],
                            'association': spaced_words[1]})
                        send_message(vk_session, 'chat_id', event.chat_id, "вы зарегестировались! Ваш ник: "
                                     + spaced_words[1] + " и уровень 1 :)")
                    else:
                        user_worker.insert(10, event.extra_values['from'], spaced_words[1])
                        users.insert(0, {
                            'access_level': 10,
                            'vk_id': event.extra_values['from'],
                            'association': spaced_words[1]})
                    send_message(vk_session, 'chat_id', event.chat_id, "вы зарегестировались админом! Ваш ник: "
                                 + spaced_words[1] + " и уровень 10 (max) :)")
                elif int(event.extra_values['from']) in list(i['vk_id'] for i in users):
                    send_message(vk_session, 'chat_id', event.chat_id, "Вы зарегестрированы :c")
                    # TODO добавить сообщение для комманды изменения ассоциации
                else:
                    send_message(vk_session, 'chat_id', event.chat_id, "Ассоциация занята")

            if response == "!delme":
                if int(event.extra_values['from']) in list(i['vk_id'] for i in users):
                    index = list(i['vk_id'] for i in users).index(int(event.extra_values['from']))
                    user_worker.delete(int(event.extra_values['from']))
                    users.pop(index)
                else:
                    print("cannot do it")
            if spaced_words[0] == '!rename' and len(spaced_words) == 3:
                if is_permitted(event.extra_values['from'], 1):
                    for pgr in users:
                        if pgr['association'] == spaced_words[1]:
                            index = list(i['association'] for i in users).index(spaced_words[1])
                            commands.pop(index)
                            users[index] = {
                                'access_level': 1,
                                'vk_id': pgr['vk_id'],
                                'association': spaced_words[2]}
                            user_worker.update(pgr['vk_id'], spaced_words[2], 1)
                            send_message(vk_session, 'chat_id', event.chat_id,
                                         "Поздравляю вы теперь: " + spaced_words[2] + ".\n И ваш уровень: 2")
                else:
                    send_message(vk_session, 'chat_id', event.chat_id, "Ты кто такой сука?")

            """ Добавление и удаление комманд """
            # TODO добавить уровни и контроль юзеров
            if spaced_words[0] == '!addcom' and len(spaced_words) >= 3:
                if is_permitted(int(event.extra_values['from']), 5):
                    if spaced_words[1] == spaced_words[2]:
                        send_message(vk_session, 'chat_id', event.chat_id, "Нельзя добавить эхо-комманду")
                    elif spaced_words[1] in list(i['name'] for i in commands):
                        send_message(vk_session, 'chat_id',
                                     event.chat_id, "Нельзя добавить существуюую комманду")
                    else:
                        command_worker.insert(10, spaced_words[1], ' '.join(spaced_words[2:]))
                        commands.insert(0, {
                            'access_level': 10,
                            'name': spaced_words[1],
                            'value': ' '.join(spaced_words[2:])})

                        send_message(vk_session, 'chat_id', event.chat_id,
                                     "Комманда " + spaced_words[1] + " добавлена!")
                else:
                    send_message(vk_session, 'chat_id', event.chat_id, "Permission denied, required level to access: 5")

            if spaced_words[0] == '!delcom' and len(spaced_words) == 2:
                if is_permitted(event.extra_values['from'], 5):
                    for item in commands:
                        if item['name'] == spaced_words[1]:
                            command_worker.delete(spaced_words[1])
                            index = list(i['name'] for i in commands).index(spaced_words[1])
                            commands.pop(index)
                            send_message(vk_session, 'chat_id', event.chat_id,
                                         "Комманда " + spaced_words[1] + " удалена!")
                            break
                else:
                    send_message(vk_session, 'chat_id', event.chat_id, "Permission denied, required level to access: 5")


async def main():
    await longpoolHandle()


asyncio.run(main())
