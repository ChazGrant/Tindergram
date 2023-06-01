import telebot

# bot = telebot.TeleBot("5391782983:AAFHwhF00_zk8RWNRGLBLToyE863S-qhUAo")


tmp_user_info = dict()

class Singleton(object):
    def __init__(self, x):
        self.x = x

    def __new__(cls, x):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


s = Singleton(5) ## class initialized, but object not created
s1 = Singleton(7) ## instance already created

print(s.x)
print(s1.x)
# bot.infinity_polling()