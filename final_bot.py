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
    'feedback': 'My way or a highway Что бы вы хотели улучшить в этом боте'
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
    #функция, работающая при получении ботом сообщения
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


@bot.message_handler(commands=['show'])
def command_show(message):
    loadJson()
    cid = message.chat.id
    history = getUserHistory
    if history == None:
        bot.send_message(cid, "Простиии! Похоже, что у тебя нет никаких записей о расходах!")
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        for mode in SHOW_MODE:
            markup.add(mode)

        msg = bot.reply_to(message, 'Расскажи на что ты хочешь потратиться', reply_markup=markup)
        bot.register_next_step_handler(msg, process_show_spending)


def calculate_spendings(queryResult):
    total_dict = {}

    for row in queryResult:
        s = row.split(',')
        cat = s[1]
        if cat in total_dict:
            total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
        else:
            total_dict[cat] = float(s[2])
    total_text = ""
    for key, value in total_dict.items():
        total_text += str(key) + " рубликов" + str(value) + "\n"
    return total_text


def process_show_spending(message):
    try:
        cid = message.chat.id
        DayWeekMonth = message.text

        if not DayWeekMonth in SHOW_MODE:
            raise Exception("Простииии, я не могу показать твои траты на \"{}\"!".format(DayWeekMonth))

        history = getUserHistory(cid)
        if history is None:
            raise Exception("Простиии! Похоже, что у тебя нет никаких записей о расходах!")

        bot.send_message(cid, "Подожди-ка! Очень напряженно думаю...")
        bot.send_chat_action(cid, 'тыкаю по кнопочкам')
        time.sleep(0.5)

        total_text = ""

        if DayWeekMonth == 'День':
            query = datetime.now().today().strftime(dateFormat)
            queryResult = [value for index, value in enumerate(history) if
                           str(query) in value]
        elif DayWeekMonth == 'Месяц':
            query = datetime.now().today().strftime(monthFormat)
            queryResult = [value for index, value in enumerate(history) if
                           str(query) in value]
        total_text = calculate_spendings(queryResult)

        spending_text = ""
        if len(total_text) == 0:
            spending_text = "У тебя нет текущих рассходов {}!".format(DayWeekMonth)
        else:
            spending_text = "Вот твои общие расходы на текущий момент {}:\nCATEGORIES,AMOUNT \n----------------------\n{}".format(
                DayWeekMonth.lower(), total_text)

        bot.send_message(cid, spending_text)
    except Exception as e:
        bot.reply_to(message, 'Упси...! ' + str(e))


@bot.message_handler(commands=['history'])
def command_history(message):
    try:
        loadJson()
        cid = message.chat.id

        history = getUserHistory(cid)
        if history is None:
            raise Exception("Извините! Похоже, что у вас нет никаких записей о расходах!")

        total_spending_text = "Вот история ваших трат : дата, КАТЕГОРИЯ, СУММА------------------------------------\ n"

        if len(history) == 0:
            total_spending_text = "Извините! Похоже, что у вас нет никаких записей о расходах!"
        else:
            for s in history:
                total_spending_text += str(s) + "\n"
        bot.send_message(cid, total_spending_text)
    except Exception as e:
        bot.reply_to(message, 'Упс! ' + str(e))

@bot.message_handler(commands=['new'])
def command_new(message):
    loadJson()
    cid = message.chat.id
    choice.pop(cid, None)  # remove temp choice
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for cat in CATEGORIES:
        markup.add(cat)
    # markup.add('Food', 'Groceries', 'Transport', 'Shopping')
    msg = bot.reply_to(message, 'Выберите категорию', reply_markup=markup)
    bot.register_next_step_handler(msg, process_category_step)

def validateAmount(amountStr):
    if len(amountStr) > 0 and len(amountStr) <= 15:
        if amountStr.isdigit():
            if re.match("^[0-9]*\\.?[0-9]*$", amountStr):
                amount = round(float(amountStr), 2)
                if amount > 0:
                    return str(amount)
    return "0"

def process_category_step(message):
    try:
        cid = message.chat.id
        cat_text = message.text
        if cat_text not in CATEGORIES:
            raise Exception("Извините, я не распознаю категорию \"{}\"!".format(cat_text))

        choice[cid] = cat_text
        message = bot.send_message(cid, 'Сколько ты потратил на {}? \n(Введи только число)'.format(str(choice[cid])))
        bot.register_next_step_handler(message, process_amount_step)
    except Exception as e:
        bot.reply_to(message, 'Упсс! ' + str(e))

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


def getUserHistory(cid):
    global global_users_dict
    if (str(cid) in global_users_dict):
        return global_users_dict[str(cid)]
    return None


def deleteHistory(cid):
    global global_users_dict
    if (str(cid) in global_users_dict):
        del global_users_dict[str(cid)]
    return global_users_dict

def addUserHistory(cid, recordText):
    global global_users_dict
    if not (str(cid) in global_users_dict):
        global_users_dict[str(cid)] = []

    global_users_dict[str(cid)].append(recordText)
    return global_users_dict


@bot.message_handler(commands=['clear'])
def command_clear(message):
    global global_users_dict
    cid = message.chat.id
    loadJson()
    clear_history_text = ""
    if (str(cid) in global_users_dict):
        writeJson(deleteHistory(cid))
        clear_history_text = "История очищена!"
    else:
        clear_history_text = "Извините! Похоже, что у вас нет никаких записей о расходах!"
    bot.send_message(cid, clear_history_text)

def process_feed_back(message):
    cid = message.chat.id
    feedback_text = message.text
    print("****************ОБРАТНАЯ СВЯЗЬ********************")
    print("chatid:{} feedback: {}".format(str(cid), feedback_text))
    print("*********************************************")
    bot.send_message(cid, 'Спасибо за отзыв!')

@bot.message_handler(commands=['feedback'])
def command_feedback(message):
    cid = message.chat.id
    message = bot.send_message(cid, 'Как я могу стать лучшим ботом? Приветствуются любые отзывы!')
    bot.register_next_step_handler(message, process_feed_back)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    bot.send_message(m.chat.id, "Я не понимаю \"" + m.text + "\"\nМожет быть, попробуйте зайти на страницу справки по адресу /help")

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()




def main():
    try:
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(5)
        print("Internet error!")


if __name__ == '__main__':
    main()