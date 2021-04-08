def get_token(fn: str = "token.token"):
    f = open(fn, 'r')
    token = f.readline()
    f.close()
    return token


def get_cmd_params(text: str, idt):

    splited_string = text.split(" ")
    params = [idt, *splited_string[1:]]
    cmd = splited_string[0]

    return cmd, params
