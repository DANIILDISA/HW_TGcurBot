import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConverter
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)  # определяем клавиатуру
start_button = KeyboardButton('/start')
values_button = KeyboardButton('/values')
keyboard.add(start_button, values_button)


@bot.message_handler(commands=['start', 'help'])  # добавляем клавиатуру в стартовое сообщение
def command_help(message: telebot.types.Message):
    text = ('Использовать бота:\n'
            '<Имя валюты>\n<имя валюты, в которую вы хотите конвертировать>\n'
            '<количество переводимой валюты>\n\n'
            'Вы можете увидеть список всех доступных валют, введя команду /values')
    bot.reply_to(message, text, reply_markup=keyboard)


@bot.message_handler(commands=['values'])
def command_values(message: telebot.types.Message):
    text = 'Доступные валюты: \n' + '\n'.join(keys.keys())
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split()

        if len(value) != 3:
            raise ConvertionException('Неверное количество параметров.')

        quote, base, amount = map(str.lower, value)
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}', reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}', reply_markup=keyboard)
    else:
        text = f'Цена {amount} {quote.capitalize()} в {base.capitalize()} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True, interval=0)

