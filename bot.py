#import pandas as pd
import re
import ephem
import logging
import settings
from datetime import date, datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

url = "https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Russia"
data = pd.read_html(url)
russian_cities_names = list(data[0]['Russian name'])

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

def words_counter(update, context):
    #убираем все знаки препинания
    print("вызыван words_counter")
    text = re.sub(r'[^\w\s]', ' ',update.message.text)
    #отдельно убираем знаки нижнего подчеркивания (с помощью регулярок чето не получилось)
    text = text.replace("_"," ").split()[1:]
    if bool(text):
        update.message.reply_text(f"количество слов: {len(text)}")
    else:
        update.message.reply_text("эй! ты прислал(а) пустое предложение, так нельзя...")

def full_moon_info(update, context):
    current_date = date.today().strftime("%Y/%m/%d")
    update.message.reply_text(str(ephem.next_full_moon(current_date))[0:10])

# def cities_game(update, context):
#     text = update.message.text.lower().split()[1]
#     city_name = []
#     while not bool(city_name):
#         for city in russian_cities_names:
#             if text[-1] == city.lower()[0]:
#                 city_name.append(city)
#                 update.message.reply_text(f"{city.capitalize()}, твой ход")
                
#                 break
#     city_name.clear()
            
                

def main():
    mybot = Updater(settings.API_KEY, use_context = True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    # команда /start
    dp.add_handler(CommandHandler('start', greet_user))
    # команда /planet название_планеты
    dp.add_handler(CommandHandler('planet', planet_info))
    # подсчет слов в предложении
    dp.add_handler(CommandHandler('wordcount', words_counter))
    # дата полнолуния
    dp.add_handler(CommandHandler('next_full_moon', full_moon_info))
    # игра в города
    #dp.add_handler(CommandHandler('cities', cities_game))
    # эхо бот
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот запущен')
    mybot.start_polling()
    mybot.idle()
if __name__ == '__main__':
    main()