from vk_api.longpoll import VkLongPoll, VkEventType

from Database.CommandDbWorker import CommandWorker
from Database.UserDbWorker import UserWorker
from StartupLoader.StartupLoader import StartupLoader
import vk_api
import random


# Предзагрузка конфигураций
config_loader = StartupLoader('config.JSON')

admin_id_int = config_loader.get_admin_id()

# Загрузка листов из БД
users = config_loader.load_users_list()
commands = config_loader.load_commands_list()

# Инициализация vk_api
vk_session = vk_api.VkApi(token= config_loader.get_vk_token())
session_api = vk_session.get_api()
long_poll = VkLongPoll(vk_session)

# Создание БД воркеров
user_worker = UserWorker()
command_worker = CommandWorker()


def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send',
                      {id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648),
                       "attachment": attachment, 'keyboard': keyboard})


def get_pictures(vk_session, id_group, vk):
    try:
        attachment = ''
        max_num = vk.photos.get(owner_id=id_group, album_id='wall', count=0)['count']
        num = random.randint(1, max_num)
        pictures = vk.photos.get(owner_id=str( id_group), album_id='wall', count=1, offset=num)['items']
        buf = []
        for element in pictures:
            buf.append('photo' + str( id_group) + '_' + str(element['id']))
        print(buf)
        attachment = ','.join(buf)
        print(type(attachment))
        print(attachment)
        return attachment
    except:
        return get_pictures(vk_session,  id_group, vk)


for event in long_poll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        # TODO не еш подумой
        # logging.info("message from user id" + str(event.extra_values['from']) + " with MSG: " + event.text)
        response = event.text

        for item in commands:
            if item['name'] == event.text:
                # from chat
                send_message(vk_session, 'chat_id', event.chat_id, item['value'])

        if event.text == "!камни":
            send_message(vk_session, 'chat_id', event.chat_id,
                         '🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿')
        if event.text == "!vkbot":
            send_message(vk_session, 'chat_id', event.chat_id,
                         'Комманды бота Ильи: \n >>>>>>>>>>>>>>>>>>>> \n <<КОМАНДЫ>> \n  '
                         '\n •!шанс ---->узнать шанс чего-либо \n •!шар --->вопрос, после чего будет '
                         'выдан ответ \n  \n <<РАНДОМ АНИМЕ АРТЫ>> \n  \n •!лоли \n •!юри \n •!ахегао '
                         '\n •!фейт прикол \n •!фейт арт \n •!камшот \n \n <<3Д ТЯНКИ И НЕ ТОЛЬКО>> \n  \n'
                         ' •!3д мусор \n •!кукла \n \n <<ТОСАКА РИН>> \n \n •!тосака \n •!тосака2 ---> хентай'
                         ' \n •!иштар \n •!эриш  \n \n <<ПРОЧЕЕ ГОВНО>> \n \n •!камни \n '
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
            send_message(vk_session, 'peer_id', event.peer_id, 'Держи арт из группы far side of the moon!', attachment)
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
        if event.text.lower() == "!gvn":
            huy = vk_session.method('video.get', {'owner_id': '-164489758', 'count': 200, 'offset': 1})['items']
            qwert = random.choice(list(i for i in huy))
            send_message(vk_session, 'peer_id', event.peer_id, 'Держи gvn!',attachment='video' + str(-164489758) + '_' + str(qwert['id']))

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
            if spaced_words[1] not in list(i['association'] for i in users):
                user_worker.insert(1, event.extra['from'], spaced_words[1])
                commands.insert(0, {
                    'access_level': 1,
                    'vk_id': event.extra['from'],
                    'value': spaced_words[1]})
            else:
                send_message(vk_session, 'chat_id', event.chat_id, "Ассоциация занята")

        """ Добавление и удаление комманд """
        # TODO добавить уровни и контроль юзеров
        if spaced_words[0] == '!addcom' and len(spaced_words) >= 3:
            if spaced_words[1] == spaced_words[2]:
                send_message(vk_session, 'chat_id', event.chat_id, "Нельзя добавить эхо-комманду")
            elif spaced_words[1] in list(i['name'] for i in commands):
                send_message(vk_session, 'chat_id', event.chat_id, "Нельзя добавить существуюую комманду")
            else:
                command_worker.insert(10, spaced_words[1], ' '.join(spaced_words[2:]))
                commands.insert(0, {
                    'access_level': 10,
                    'name': spaced_words[1],
                    'value': ' '.join(spaced_words[2:])})

                send_message(vk_session, 'chat_id', event.chat_id, "Комманда " + spaced_words[1] + " добавлена!")

        if spaced_words[0] == '!delcom' and len(spaced_words) == 2:
            for item in commands:
                if item['name'] == spaced_words[1]:
                    command_worker.delete(spaced_words[1])
                    index = list(i['name'] for i in commands).index(spaced_words[1])
                    commands.pop(index)
                    send_message(vk_session, 'chat_id', event.chat_id, "Комманда " + spaced_words[1] + " удалена!")
                    break
