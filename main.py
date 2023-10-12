import telebot
import config

from db import *
from telebot import types

bot = telebot.TeleBot(config.token)


# здрасте
@bot.message_handler(commands=['start'])
def welcome(message):
    text = 'Вы уже зарегистрированы'
    bot.send_message(message.chat.id, "Здравствуйте😝")
    user_id = message.chat.id
    user = getUser(user_id)
    print(user)

    if getUser(user_id) == None:
        insertUser(user_id)
        text = f"{message.from_user.first_name}, вы зарегистрированы\n Какие дальнейшие действия?"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    itemNews = types.KeyboardButton('Новости')
    itemSub = types.KeyboardButton('Мои подписки')
    itemCat = types.KeyboardButton('Категории')

    markup.add(itemCat, itemNews, itemSub)

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    user_id = message.chat.id
    categ = getCategories()
    textcat = 'Список категорий,на какую хотите подписаться? \n'
    if message.text == 'Категории':
        menu = types.KeyboardButton('Основное меню')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(menu)
        for i in categ:
            textcat += f'{i[0]}🫥 {i[2]} \n'
            btn = types.KeyboardButton(f'Подписаться на {i[2]}')
            markup.add(btn)
        bot.send_message(message.chat.id, textcat, reply_markup=markup)

    if message.text.startswith('Подписаться на'):
        cat = message.text[15:]
        print(cat)
        cat_id = getIdCat(cat)[0]
        print(cat_id)
        s = searchSab(user_id, cat_id)
        print(s)
        if searchSab(user_id, cat_id) == None:
            insertSub(user_id, cat_id)
            text = f"Вы подписались на {cat}"
        else:
            text = f"Вы уже подписаны на {cat}"
        bot.send_message(message.chat.id, text)
    if message.text == "Основное меню":
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      itemNews = types.KeyboardButton('Новости')
      itemSub = types.KeyboardButton('Мои подписки')
      itemCat = types.KeyboardButton('Категории')

      markup.add(itemCat, itemNews, itemSub)

      bot.send_message(message.chat.id, 'Что хотите?', reply_markup=markup)

    if message.text == 'Мои подписки':
        sabs = getSubUser(user_id)
        menu = types.KeyboardButton('Основное меню')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(menu)
        for i in sabs:
            markup.add(types.KeyboardButton(f"Отписаться от {i[0]}"))
        bot.send_message(message.chat.id, 'Ваши подписки', reply_markup=markup)

    if message.text.startswith('Отписаться от'):
        deletedsub = message.text[14:]
        cat_id = getIdCat(deletedsub)
        print(cat_id)
        if searchSab(user_id, cat_id[0]) == None:
            text = f"Вы еще не подписаны на {deletedsub}"
            bot.reply_to(message, text)
        else:
            delSub(user_id, cat_id)
            sub = getSubUser(user_id)
            menu = types.KeyboardButton('Основное меню')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(menu)
            for i in sub:
                print(type(i[0]))
                markup.add(types.KeyboardButton(f"Отписаться от {i[0]}"))
            bot.send_message(message.chat.id, f"Вы успешно отписаны от {deletedsub}", reply_markup=markup)



bot.infinity_polling()
