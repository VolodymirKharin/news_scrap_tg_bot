import time
import news_db
import news_scrapper
from config import token
import telebot

from telebot import types
from telebot import apihelper

bot = telebot.TeleBot(token)
apihelper.proxy = {'http': 'socks5://203.32.121.231:80'}


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_buttons = ["The latest 5 news", "The latest 50 news", "Fresh news"]
    bot.send_message(message.chat.id, "Scrapping.....")
    news_scrapper.run()
    keyboard.add(*start_buttons)
    bot.send_message(message.chat.id, "Done!", disable_notification=True, reply_markup=keyboard)
    news = news_db.get_fifty_news()
    for i in news:
        msg = f"{i['date_time']}\n" \
              f"{i['title']}\n{i['link']}\n"
        bot.send_message(message.chat.id, msg)
    news_every_minute(message)


@bot.message_handler(content_types=['text'])
def get_last_five_news(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'The latest 5 news':
            news = news_db.get_five_news()
            for i in news:
                msg = f"{i['date_time']}\n" \
                      f"{i['title']}\n{i['link']}\n"
                bot.send_message(message.chat.id, msg)

        elif message.text == 'The latest 50 news':
            news = news_db.get_fifty_news()
            for i in news:
                msg = f"{i['date_time']}\n" \
                      f"{i['title']}\n{i['link']}\n"
                bot.send_message(message.chat.id, msg)

        elif message.text == 'Fresh news':
            no_fresh_news = True
            news_scrapper.run(10)
            get_last_news = news_scrapper.last_news
            for i in get_last_news:
                if i:
                    no_fresh_news = False
                    my_new = news_db.get_news_by_id(i)
                    msg = f"{my_new[0]['date_time']}\n" \
                          f"{my_new[0]['title']}\n{my_new[0]['link']}\n"
                    bot.send_message(message.chat.id, msg)
            if no_fresh_news:
                bot.send_message(message.chat.id, 'No fresh news')


def news_every_minute(message):
    while True:
        no_fresh_news = True
        news_scrapper.run(10)
        get_last_news = news_scrapper.last_news
        for i in get_last_news:
            if i:
                no_fresh_news = False
                my_new = news_db.get_news_by_id(i)
                msg = f"{my_new[0]['date_time']}\n" \
                      f"{my_new[0]['title']}\n{my_new[0]['link']}\n"
                bot.send_message(message.chat.id, msg)
        if no_fresh_news:
            bot.send_message(message.chat.id, 'Past 15 sec.No fresh news')
        time.sleep(15)


def main():
    bot.polling(non_stop=True)


if __name__ == '__main__':
    bot.polling(non_stop=True)
