import telebot
from extensions import Converter, APIException
from config import keys

bot = telebot.TeleBot('5805536974:AAGbmEt1003-EU4Q1Y14dAX2yyvKpsOR7ro')


@bot.message_handler(commands= ['start', 'help'])
def handler(message):
    bot.reply_to(message, 'Чтобы начать работу, введите команду боту в следующем формате: \n <имя валюты>\
<в какую валюту переводить><количество переводимой валюты> \n Список доступных валют: /values')

@bot.message_handler(commands = ['values'])
def handler_values(message):
    text = 'Доступные валюты: \n'
    for key in keys.keys():
        text += f'{key}\n'
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text'])
def handler_convert(message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise APIException('Неправильное количество параметров')

        quote, base, amount = values

        total_base = Converter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except:
        bot.reply_to(message, 'Ошибка сервера')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)