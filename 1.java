import telebot, subprocess
from random import randint
from telebot.types import Message
from googletrans import Translator
from telebot import types
import config, os


token = '7172159834:AAHNKUv_v4Fjb12irpKvAuyipwtHn2B4AYw'

bot = telebot.TeleBot(token)

def trans_later(eng_text):
    translator = Translator()
    tr = translator.translate(eng_text, dest="ru")
    return tr.text
def analiz():
    return (subprocess.run(
        "pmd.bat check -d file.java -R rulesets/java/quickstart.xml -f text",
        shell=True, capture_output=True, text=True, encoding='cp866').stdout)

def analiz_itog(message):
    with open('file.java', 'w', encoding='utf-8') as file:
        file.write(message.text)
    analizator_text = analiz() + '\n'
    analizator_text += "Перевод на русский язык:" + '\n' + trans_later(analizator_text)
    bot.reply_to(message, analizator_text)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Методы рефакторинга")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бот который разбирается в java, могу рассказать о методах рефакторинга".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['document'])
def get_text_messages(message: Message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    if message.document.file_name[-5:] == '.java':
        src = ('C:/Users/korudenko/PycharmProjects/telegram_bot/file.java')
            # + message.document.file_name)
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        # analiz_itog(message)
        bot.reply_to(message, "Пожалуй, я сохраню это")
    else:
        bot.reply_to(message, "Файл не проанализирован, я понимаю только файлы на ЯП java")

@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def get_text_messeges(message: Message):
    if (message.text == "Методы рефакторинга"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Выделение метода")
        btn2 = types.KeyboardButton("Выделение класса")
        back = types.KeyboardButton("Объединение условных выражений")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="О каком методе {0.first_name} хочет узнать?".format(message.from_user), reply_markup=markup)
    elif (message.text == "Выделение метода"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("назад")

        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    else:
        analiz_itog(message)
    if message.from_user.id != 321354512:
        bot.send_message(321354512, f'{message.from_user.id} @{message.from_user.username} '
        f'{message.from_user.first_name} {message.from_user.last_name} {message.text} \n'), message.text



bot.polling()