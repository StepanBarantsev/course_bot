import telebot
import schedule
import time
from faunahelper import FaunaHelper
from faunadb.client import FaunaClient
import datetime as d
import os

bot_token = os.environ['BOT_TOKEN']
faunakey = os.environ['FAUNAKEY']


def job(bot, faunahelper):
    students = faunahelper.get_all_students()

    for student in students:
        if not student['freezed']:
            try:
                if student['days'] < 0:
                    faunahelper.freeze_student_by_telegram_id(student['telegram_id'])
                elif student['days'] == 0:
                    bot.send_message(student['telegram_id'],
                                     '''Добрый день! У Вас закончилось время поддержки. Следует продлить время (600 рублей) или приобрести новый блок.
Кроме того, Вы можете запросить у бота записи лекций и дз за текущий блок, чтобы продолжить прохождение курса самостоятельно.''')
                elif student['days'] == 7 or student['days'] % 10 == 0 or student['days'] == 1:
                    bot.send_message(student['telegram_id'], 'Добрый день. Напоминаю, что до конца курса у Вас осталось %s дней: ' % str(student['days']))
            except telebot.apihelper.ApiException:
                bot.send_message(375764533,
                                 'Добрый день. Напоминаю, что до конца курса у %s осталось %s дней!' % (student['name'], str(student['days'])))
            faunahelper.decrement_days_by_telegram_id(student['telegram_id'])

    bot.send_message(375764533, "Программа была запущена %s" % str(d.date.today()))


bot = telebot.TeleBot(bot_token)
faunahelper = FaunaHelper(FaunaClient(faunakey))

# Строка для тестирования
# schedule.every(10).seconds.do(job, bot, faunahelper)
schedule.every().day.at("12:00").do(job, bot, faunahelper)

while True:
    schedule.run_pending()
    # Сколько то часов паузы
    bot.send_message(375764533, "Программа в рабочем состоянии %s" % str(d.date.today()))
    time.sleep(3600 * int(os.environ['HOURS']))
    # Тоже строка для тестирования
    # time.sleep(1 * int(os.environ['HOURS']))
