import telebot
from settings import bot_token
from settings import faunakey
from faunadb import query
from faunadb.objects import Ref
from faunadb.client import FaunaClient


bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['getdays'])
def getdays(message):
    clientf = FaunaClient(secret=faunakey)
    result = clientf.query(query.get(query.match(query.index('telegram_id'), message.chat.id)))
    bot.send_message(message.chat.id, str(result['data']['days'] + 1))


if __name__ == '__main__':
    bot.polling(none_stop=True)

