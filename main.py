import telebot
from machine import Pizza

token = '1770183866:AAELXKoWHOwCGzGKWXgqATaI9UdVDlX9L1U'
url = 't.me/alkosakdfsokfmwdfi_bot'

bot = telebot.TeleBot(token, parse_mode=None)

pizza = Pizza()


@bot.message_handler()
def entry(message):
    pizza.input(message.text)
    bot.reply_to(message, pizza.output_text)


bot.polling()
