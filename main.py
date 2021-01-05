import telebot
from faunahelper import FaunaHelper
from faunadb.client import FaunaClient
from faunadb.errors import NotFound
from lmshelper import LmsHelper
import os

bot_token = os.environ['BOT_TOKEN']
faunakey = os.environ['FAUNAKEY']
lmskey = os.environ['LMSKEY']

bot = telebot.TeleBot(bot_token)
faunahelper = FaunaHelper(FaunaClient(faunakey))
lmshelper = LmsHelper(lmskey)


@bot.message_handler(commands=['start', 'help'])
def getdays(message):
    chat_id = message.chat.id
    text = '''Добрый день, это бот Python для начинающих.
Бот поддерживает следующие команды:
/help -- получить справку по командам
/getdays -- бот отдаст количество дней до окончания срока поддержки
/getavailableblocks -- бот отдаст все блоки со всеми видеозаписями и дз, которые у Вас приобретены
/getsolutions -- сама по себе команда без аргументов является некорреткной. Вызывать ее следует вот так: /getsolutions <Номер задания>, например:
/getsolutions 1.1 чтобы получить решение по заданию 1.1. Решение будет Вам доступно только после того, как Вы сами прорешаете задачу на оценку 5.

Ссылка на репозиторий, где содержится код бота: https://github.com/StepanBarantsev/course_bot

Плейлист с видео, где я разрабатывал этого бота: https://www.youtube.com/playlist?list=PLEUFMPQp6Iv7DKaPundqvWMbOMNXQH9HF

Если с ботом какие-то проблемы или есть какие-то пожелания к нему, то пишите мне в личные сообщения в telegram

При нахождении ошибки в решении задач, также присылайте в личные сообщения тест, который ронял бы решение. Программа будет исправлена, тест добавлен в проверяющую систему, а Вы получите дополнительное время поддержки.'''
    bot.send_message(chat_id, text)


@bot.message_handler(commands=['getdays'])
def getdays(message):
    chat_id = message.chat.id
    try:
        bot.send_message(chat_id, "До конца курса осталось %s дней." % str(faunahelper.get_days_by_telegram_id(chat_id) + 1))
    except NotFound:
        bot.send_message(chat_id, "Извините, информации о Вас нет в базе данных. Чтобы тренер мог добавить Вас в базу сообщите ему следующее число: {chat_id}")


@bot.message_handler(commands=['getavailableblocks'])
def getavailableblocks(message):
    chat_id = message.chat.id
    try:
        lmsid = faunahelper.get_lmsid_by_telegram_id(chat_id)
        max_payed_block = lmshelper.return_max_payed_block(lmsid)

        info = faunahelper.get_info()
        bot.send_message(chat_id, info['blocks']['1'])
        if max_payed_block > 1:
            bot.send_message(chat_id, info['blocks']['2'])
        if max_payed_block > 2:
            bot.send_message(chat_id, info['blocks']['3'])
        if max_payed_block > 3:
            bot.send_message(chat_id, info['blocks']['4'])
    except NotFound:
        bot.send_message(chat_id, "Извините, информации о Вас нет в базе данных. Чтобы тренер мог добавить Вас в базу сообщите ему следующее число: {chat_id}")


@bot.message_handler(commands=['getsolutions'])
def getsolutions(message):
    chat_id = message.chat.id
    try:
        task = message.text.split()[1]
        lmsid = faunahelper.get_lmsid_by_telegram_id(chat_id)
        if lmshelper.is_task_completed(lmsid, task, 5):
            info = faunahelper.get_info()
            bot.send_message(chat_id, info['solutions'][task])
        else:
            bot.send_message(chat_id, "У Вас не выполнено данное задание на необходимый балл (5)")
    except NotFound:
        bot.send_message(chat_id, f"Извините, информации о Вас нет в базе данных. Чтобы тренер мог добавить Вас в базу сообщите ему следующее число: {chat_id}")
    except IndexError:
        bot.send_message(chat_id, "Аргумент не был введен! Введите аргумент после команды /getsolutions (номер задания, которое Вы хотиите посмотреть)")
    except TypeError:
        bot.send_message(chat_id, "Такого задания не существует.")
    except:
        bot.send_message(chat_id, "Неизвестная ошибка!")


if __name__ == '__main__':
    bot.polling(none_stop=True)

