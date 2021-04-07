from bot import bot


def get_token(fn: str = "token.token"):
    f = open(fn, 'r')
    token = f.readline()
    f.close()
    return token

if __name__ == '__main__':
    print('Running bot.')
 
    bot.token = get_token()
    bot.polling(none_stop=False, interval=0)


