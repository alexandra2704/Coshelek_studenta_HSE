def addUserHistory(cid, recordText):
    global global_users_dict
    if not (str(cid) in global_users_dict):
        global_users_dict[str(cid)] = []

    global_users_dict[str(cid)].append(recordText)
    return global_users_dict

def process_feed_back(message):
    cid = message.chat.id
    feedback_text = message.text
    print("****************ОБРАТНАЯ СВЯЗЬ********************")
    print("chatid:{} feedback: {}".format(str(cid), feedback_text))
    print("*********************************************")
    bot.send_message(cid, 'Спасибо за отзыв!')