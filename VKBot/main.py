from vk_api.longpoll import VkLongPoll, VkEventType
from Database.CommandDbWorker import CommandWorker
from datetime import datetime
import vk_api
import random
import get_pictures
import get_pictures2
import get_hentai
import get_itpedia
import get_fateprikol
import get_fateart
import get_3d
import get_kuk
import get_rin
import get_rin18
import get_erish
import get_ishtar
import cumshot
import settings


# load all commands

command_worker = CommandWorker()
commands = command_worker.select_all()

vk_session = vk_api.VkApi(token=settings.get_token())
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send',
                      {id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648),
                       "attachment": attachment, 'keyboard': keyboard})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('Время: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
        print('Текст ПИДОРАСА: ' + str(event.text))
        print(event.user_id)
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
            attachment = get_pictures.get(vk_session, -127518015, session_api)
            vk_session.method('messages.send', {'chat_id': event.chat_id, 'message': 'Держи девочку!', 'random_id': 0,
                                                "attachment": attachment})
        if event.text == "!юри":
            attachment = get_pictures2.get(vk_session, -153284406, session_api)
            vk_session.method('messages.send', {'chat_id': event.chat_id, 'message': 'держи лесбух!', 'random_id': 0,
                                                "attachment": attachment})
        if event.text == "!ахегао":
            attachment = get_hentai.get(vk_session, -128535882, session_api)
            vk_session.method('messages.send',
                              {'chat_id': event.chat_id, 'message': 'держи ахегао, конченый извращенец!',
                               'random_id': 0, "attachment": attachment})
        if event.text == "!палата шевцова":
            attachment = get_itpedia.get(vk_session, -88245281, session_api)
            vk_session.method('messages.send',
                              {'chat_id': event.chat_id, 'message': 'держи мем из палаты Шевцова!', 'random_id': 0,
                               "attachment": attachment})
        if event.text == "!фейт прикол":
            attachment = get_fateprikol.get(vk_session, -183563128, session_api)
            vk_session.method('messages.send',
                              {'chat_id': event.chat_id, 'message': 'держи мем из группы Fate/GrandПрикол!',
                               'random_id': 0, "attachment": attachment})
        if event.text == "!фейт арт":
            attachment = get_fateart.get(vk_session, -191752227, session_api)
            vk_session.method('messages.send',
                              {'chat_id': event.chat_id, 'message': 'держи арт из группы far side of the moon!',
                               'random_id': 0, "attachment": attachment})
        if event.text == "!3д мусор":
            attachment = get_3d.get(vk_session, -70232735, session_api)
            vk_session.method('messages.send',
                              {'chat_id': event.chat_id, 'message': 'держи свой 3д мусор!', 'random_id': 0,
                               "attachment": attachment})
        if event.text == "!кукла":
            attachment = get_kuk.get(vk_session, -186765691, session_api)
            vk_session.method('messages.send',
                              {'chat_id': event.chat_id, 'message': 'держи свою куклу, куклоёб!', 'random_id': 0,
                               "attachment": attachment})
        if event.text == "!хуесосина":
            send_message(vk_session, 'chat_id', event.chat_id, attachment='video210923765_456239281')
        if event.text == "!колда":
            send_message(vk_session, 'chat_id', event.chat_id, attachment='video537612639_456239020')
        if event.text == "!музыка":
            send_message(vk_session, 'chat_id', event.chat_id,
                         attachment='audio564230346_456239018,audio564230346_456239019,audio564230346_456239017')
        if event.text == "!тосака":
            attachment = get_rin.get(vk_session, -119603422, session_api)
            vk_session.method('messages.send', {'chat_id': event.chat_id, 'message': 'держи Тосаку!', 'random_id': 0,
                                                "attachment": attachment})
        if event.text == "!тосака2":
            attachment = get_rin18.get(vk_session, -119603422, session_api)
            vk_session.method('messages.send',
                              {'chat_id': event.chat_id, 'message': 'держи хентайную Тосаку!', 'random_id': 0,
                               "attachment": attachment})
        if event.text == "!иштар":
            attachment = get_ishtar.get(vk_session, -119603422, session_api)
            vk_session.method('messages.send', {'chat_id': event.chat_id, 'message': 'держи Иштар!', 'random_id': 0,
                                                "attachment": attachment})
        if event.text == "!эриш":
            attachment = get_erish.get(vk_session, -119603422, session_api)
            vk_session.method('messages.send',
                              {'chat_id': event.chat_id, 'message': 'держи Эрешкигаль!', 'random_id': 0,
                               "attachment": attachment})
        if event.text == "!радмир":
            send_message(vk_session, 'chat_id', event.chat_id, attachment='photo564230346_457239374')
        if event.text == "!клоун":
            send_message(vk_session, 'chat_id', event.chat_id, attachment='photo564230346_457239422')

        if event.text == "!камшот":
            attachment = cumshot.get(vk_session, -2343758, session_api)
            vk_session.method('messages.send',
                              {'chat_id': event.chat_id, 'message': 'держи рандом скриншот!', 'random_id': 0,
                               "attachment": attachment})
        if event.text == "!кто":
            val = random.choice((vk_session.method('messages.getChat', {'chat_id': event.chat_id}))['users'])
            vk_session.method('messages.send',
                              {'chat_id': event.chat_id, 'message': "@id" + str(val), 'random_id': 0})
        if event.text.lower() == "!gvn":
            huy = vk_session.method('video.get',{'owner_id':'-164489758', 'count':200, 'offset':1})['items']
            qwert = random.choice(list(i for i in huy))
            vk_session.method('messages.send', {'chat_id': event.chat_id, 'message': 'Держи gvn!', 'random_id': 0, "attachment": 'video' + str(-164489758) + '_' + str(qwert['id'])}) 

        spaced_words = str(response).split(' ')

        if spaced_words[0] == '!шанс' and len(spaced_words) > 1:
            vk_session.method('messages.send', {'chat_id': event.chat_id,
                                                'message': 'Шанс того, что ' + ' '.join(spaced_words[1:]) + ' - '
                                                           + str(random.randint(1, 100)) + '%', 'random_id': 0})
        if spaced_words[0] == '!шар':
            vk_session.method('messages.send', {'chat_id': event.chat_id,
                                                'message': 'Мойт ответ - ' +
                                                           str(random.choice(["Да",
                                                                              "Нет",
                                                                              "Скорее всего, но это не точно",
                                                                              "В душе не ебу если честно",
                                                                              "Да, это прям 100%",
                                                                              "нет,ты чё шизоид?"]))
                                                           + ' ', 'random_id': 0})

        """ Добавление и удаление комманд """
        # TODO добавить уровни и контроль юзеров
        if spaced_words[0] == '!addcom' and len(spaced_words) >= 3:
            if spaced_words[1] == spaced_words[2]:
                send_message(vk_session, 'chat_id', event.chat_id, "Нельзя добавить эхо-комманду")
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
