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
            total_dict[cat] = round(total_dict[cat] + float(s[2]),2)   
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
