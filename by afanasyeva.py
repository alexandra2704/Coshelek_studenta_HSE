def addUserHistory(cid, recordText):
    global global_users_dict
    if not (str(cid) in global_users_dict):
        global_users_dict[str(cid)] = []

    global_users_dict[str(cid)].apend(recordText)
    return global_users_dict