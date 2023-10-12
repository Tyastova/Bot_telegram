import telebot
bot = telebot.TeleBot('6570842377:AAEGQR2HfPpt7fncFt-Kq4C7mZj8L8PfgGM', parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Здрасте")


bot.infinity_polling()
