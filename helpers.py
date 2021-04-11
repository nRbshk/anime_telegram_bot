def get_token(fn: str = "token.token"):
    return open(fn, 'r').readline()

def get_date():
    import datetime
    """
    return date in format day.month.year
    """
    time = str(datetime.datetime.now())
    time = time[0:10]
    year, day, month = time.split("-")
    return f'{day}.{month}.{year}'