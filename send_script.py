import telebot
import schedule
from settings import bot_token
import time
from faunahelper import FaunaHelper
from faunadb.client import FaunaClient
from settings import faunakey
import datetime as d


def job(bot, faunahelper):
    students = faunahelper.get_all_students()

    for student in students:
        try:
            if student['days'] == 0:
                bot.send_message(student['telegram_id'],
                                 '''Добрый день! У Вас закончилось время поддержки. Следует продлить время (600 рублей) или приобрести новый блок.
    Кроме того, Вы можете запросить у бота записи лекций и дз за текущий блок, чтобы продолжить прохождение курса самостоятельно.''')
            elif student['days'] == 7 or student['days'] % 10 == 0 or student['days'] == 1:
                bot.send_message(student['telegram_id'], 'Добрый день. Напоминаю, что до конца курса у Вас осталось %s дней: ' % str(student['days']))
        except telebot.apihelper.ApiException:
            bot.send_message(375764533,
                             'Добрый день. Напоминаю, что до конца курса у %s осталось %s дней: ' % (student['name'], str(student['days'])))
        faunahelper.decrement_days_by_telegram_id(student['telegram_id'])

    bot.send_message(375764533, "Программа была запущена %s" % str(d.date.today()))


bot = telebot.TeleBot(bot_token)
faunahelper = FaunaHelper(FaunaClient(faunakey))

schedule.every(60).seconds.do(job, bot, faunahelper)

while True:
    schedule.run_pending()
    time.sleep(1)
