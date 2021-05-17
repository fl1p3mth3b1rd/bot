#import ephem
import logging
import settings
#from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print('вызван /start')
    update.message.reply_text("Привет!")
    print(update)

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(f"вы сказали: {text}")




def main():
    mybot = Updater(settings.API_KEY, use_context = True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    # команда /start
    dp.add_handler(CommandHandler('start', greet_user))
    # команда /planet название_планеты
    #dp.add_handler(CommandHandler('planet', planet_info))
    # эхо бот
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот запущен')
    mybot.start_polling()
    mybot.idle()
if __name__ == '__main__':
    main()