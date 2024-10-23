def validateAmount(amountStr):
    if len(amountStr) > 0 and len(amountStr) <= 15:
        if amountStr.isdigit:
            if re.match("^[0-9]*\\.?[0-9]*$", amountStr):
                amount = round(float(amountStr), 2)
                if amount > 0:
                    return str(amount)
    return 0

'''
