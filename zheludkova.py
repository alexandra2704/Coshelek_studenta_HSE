def getUserHistory(cid):
    global global_users_dict
    if (str(cid) in global_users_dict):
        return global_users_dict[str(cid)]
    return None
