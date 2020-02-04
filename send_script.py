import telebot
import schedule
from settings import bot_token
import time


def job(bot):
    with open('database.txt') as db:
        number = db.read()
        bot.send_message(821086704, 'Осталось дней: ' + number)
        number = int(number)

    with open('database.txt', 'w') as db:
        db.write(str(number - 1))


bot = telebot.TeleBot(bot_token)

schedule.every(30).seconds.do(job, bot)

while True:
    schedule.run_pending()
    time.sleep(1)
