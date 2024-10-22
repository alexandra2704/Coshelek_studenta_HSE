
import logging
import sys
import time
import re
import os
import telebot
import json
import sched, time
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

API_TOKEN = "7592627450:AAEo1AIEOBhGZra4EfNH9vdclfoCRxl7XNU"

commands = {
    'help': 'Открывает данное меню',
    'new': 'Записать новые траты',
    'show': 'Показывает сумму расходов',
    'history': 'Показывает историю кошелька',
    'clear': 'Стирает все ваши расходы)))))',
    'feedback': 'Yay or Nay? Что бы вы хотели улучшить в этом боте'
}

dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'

choice = {}
global_users_dict = {}
CATEGORIES = ['Food', 'Groceries', 'Transport', 'Shopping']
SHOW_MODE = ['Day', 'Month']
bot = telebot.TeleBot(API_TOKEN)


telebot.logger.setLevel(logging.INFO)



def listener(messages):
    '''
    When new messages arrive TeleBot will call this function.
    '''
    for m in messages:
        if m.content_type == 'text':
            print("{} name:{} chatid:{} \nmessage: {}\n".format(str(datetime.now()), str(m.chat.first_name),
                                                                str(m.chat.id), str(m.text)))


bot.set_update_listener(listener)


def writeJson(global_users_dict):
    try:
        with open('data.json', 'w') as json_file:
            json.dump(global_users_dict, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print('!!!!!!!!!!!!!!!!!!! File data.json not found !!!!!!!!!!!!!!!!!!!')


def loadJson():
    global global_users_dict
    try:
        if not os.stat('data.json').st_size == 0:
            with open('data.json') as json_file:
                data = json.load(json_file)
            global_users_dict = data
    except FileNotFoundError:
        print('!!!!!!!!!!!!!!!!!!! File data.json not found !!!!!!!!!!!!!!!!!!!')



@bot.message_handler(commands=['start', 'help'])
def command_start(m):
    loadJson()
    global global_users_dict
    cid = m.chat.id

    help_text = "Кревет!!!!!\nЗдесь тебе доступны следующие команды!!! \n\n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)



def process_amount_step(message):
    try:
        cid = message.chat.id
        amount_text = message.text
        amount_num = validateAmount(message.text)
        if amount_num == 0:
            raise Exception("Сумма такой быть не может")

        dt = datetime.today().strftime(dateFormat + ' ' + timeFormat)
        dtText, catText, amtText = str(dt), str(choice[cid]), str(amount_num)
        writeJson(addUserHistory(cid, "{},{},{}".format(dtText, catText, amtText)))
        bot.send_message(cid, 'Записано: Ты потратил ${} на {} {}'.format(amtText, catText, dtText))

    except Exception as e:
        bot.reply_to(message, 'Opps! ' + str(e))






def main():
    try:
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(5)
        print("Internet error!")


if __name__ == '__main__':
    main()
