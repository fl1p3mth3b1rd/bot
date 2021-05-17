import ephem
import logging
import settings
from datetime import date
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

def planet_info(update, context):
    current_date = date.today().strftime("%Y/%m/%d")
    text = update.message.text.lower().split()[1]
    if text in "jupiter":
        planet = ephem.Jupiter(current_date)
    elif text in "mars":
        planet = ephem.Mars(current_date)
    elif text in "mercury":
        planet = ephem.Mercury(current_date)
    elif text in "neptune":
        planet = ephem.Neptune(current_date)
    elif text in "pluto":
        planet = ephem.Pluto(current_date)
    elif text in "saturn":
        planet = ephem.Saturn(current_date)
    elif text in "uranus":
        planet = ephem.Uranus(current_date)
    elif text in "venus":
        planet = ephem.Venus(current_date)
    pl_inf = ephem.constellation(planet)
    update.message.reply_text(f"информация по планете: {pl_inf}")


def main():
    mybot = Updater(settings.API_KEY, use_context = True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    # команда /start
    dp.add_handler(CommandHandler('start', greet_user))
    # команда /planet название_планеты
    dp.add_handler(CommandHandler('planet', planet_info))
    # эхо бот
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот запущен')
    mybot.start_polling()
    mybot.idle()
if __name__ == '__main__':
    main()