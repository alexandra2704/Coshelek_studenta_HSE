def validateAmount(amountStr):
    if len(amountStr) > 0 and len(amountStr) <= 15:
        if amountStr.isdigit:
            if re.match("^[0-9]*\\.?[0-9]*$", amountStr):
                amount = round(float(amountStr), 2)
                if amount > 0:
                    return str(amount)
    return 0

'''
'''
def process_category_step(message):
    try:
        cid = message.chat.id
        cat_text = message.text
        if not cat_text in CATEGORIES:
            raise Exception("Извините, я не узнаю эту категорию \"{}\"!".format(cat_text))

        choice[cid] = cat_text
        message = bot.send_message(cid, 'Сколько ты потратил на {}? \n(Введи только число)'.format(str(choice[cid])))
        bot.register_next_step_handler(message, process_amount_step)
    except Exception as e:
        bot.reply_to(message, 'Упсссс! ' + str(e))

'''
