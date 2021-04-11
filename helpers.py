def get_token(fn: str = "token.token"):
    return open(fn, 'r').readline()