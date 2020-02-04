import telebot
from settings import bot_token
from faunahelper import FaunaHelper
from faunadb.client import FaunaClient
from settings import faunakey

bot = telebot.TeleBot(bot_token)
faunahelper = FaunaHelper(FaunaClient(faunakey))


@bot.message_handler(commands=['getdays'])
def getdays(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "До конца курса осталось %s дней." % str(faunahelper.get_days_by_telegram_id(chat_id) + 1))


if __name__ == '__main__':
    bot.polling(none_stop=True)

