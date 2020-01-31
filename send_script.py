import telebot
import schedule
from settings import bot_token
import time
from settings import faunakey
from faunadb import query
from faunadb.objects import Ref
from faunadb.client import FaunaClient


def job(bot, clientf):

    # Получаем все данные из бд
    students = get_all_data_from_faunadb(clientf)

    for student in students:
        student = student['data']
        bot.send_message(student['id'], 'Осталось дней: ' + str(student['days']))
        new_days = student['days'] - 1
        update_data(clientf, student, new_days)


def update_data(clientf, element, new_days):
    clientf.query(query.update(query.select('ref', query.get(query.match(query.index('telegram_id'), element['id']))),
                               {'data': {'days': new_days}}))


def get_all_data_from_faunadb(clientf):
    return clientf.query(query.map_(query.lambda_("x", query.get(query.var("x"))),
                                    query.paginate(query.match(query.index("all_students")))))['data']


bot = telebot.TeleBot(bot_token)
faunaclient = FaunaClient(secret=faunakey)
schedule.every(5).seconds.do(job, bot, faunaclient)

while True:
    schedule.run_pending()
    time.sleep(1)
