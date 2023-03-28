import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('<Имя валюты>\n<имя валюты, в которую вы хотите конвертировать>\n<количество переводимой валюты>\n'
            'Вы можете увидеть список всех доступных валют, введя команду /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: \n' + '\n'.join(keys.keys())
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров.')

        quote, base, amount = map(str.lower, values)
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Цена {amount} {quote.capitalize()} в {base.capitalize()} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True, interval=0)