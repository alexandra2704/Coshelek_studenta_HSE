handle "/clear" command
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
