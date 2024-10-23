#comment
@bot.message_handler(commands=['история'])
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

@bot.message_handler(commands=['новый'])
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
    bot.register_next_step_handler(msg, process_category_step)``
