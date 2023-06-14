import telebot
from telebot import types
import json
from currency_converter import CurrencyConverter

bot = telebot.TeleBot('6274090671:AAFITGzdt6so6hfT1AECFnX3WaYY6r07drY')

currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Введите сумму подлежащую конвертации')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверно введен формат, введите число!')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/RUB', callback_data='usd/rub')
        btn4 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
        btn5 = types.InlineKeyboardButton('EUR/RUB', callback_data='eur/rub')
        btn6 = types.InlineKeyboardButton('RUB/EUR', callback_data='rub/eur')
        btn7 = types.InlineKeyboardButton('EUR/GBP', callback_data='eur/gbp')
        btn8 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
        bot.send_message(message.chat.id, 'Выберите типы валют для конвертации', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'Число должно быть положительным и больше нуля')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {amount} {values[0]} = {round(res, 2)} {values[1]} ! Можете ввести другие данные')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значении валют через /, например GBP/USD')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {amount} {values[0]} = {round(res, 2)} {values[1]} ! Можете ввести другие данные')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Введеные данные не корректны, повторите ввод значении валют через /, например GBP/USD')
        bot.register_next_step_handler(message, my_currency)

bot.polling(none_stop=True)




