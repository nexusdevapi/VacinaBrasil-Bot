import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup
from datetime import datetime
from core.engine import *

TOKEN = "8513074082:AAFLGcnPjAjGuTar9LjOTzMEXIGOzx56FOM"
bot = telebot.TeleBot(TOKEN)

user_data = {}
idade = 0

# /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    user_data[user_id] = {"started_once": True}

    menu(message.chat.id)

# Cria botões inline para escolha da faixa etária/grupo
def menu(chat_id):
    markup = quick_markup({
        'Gestante 🤰': {'callback_data': 'grupo_gestante'},
        'Criança 👶': {'callback_data': 'grupo_crianca'},
        'Jovens 🧑': {'callback_data': 'grupo_adolescente'},
        'Adulto 🧑‍💼': {'callback_data': 'grupo_adulto'},
        'Idoso 👴': {'callback_data': 'grupo_idoso'}
    }, row_width=3)
    
    bot.send_message(chat_id, "Escolha o grupo para consultar as vacinas:", reply_markup=markup)

@bot.message_handler(commands=['procurar'])
def procurar(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Use: /procurar nome da vacina')
        return
    vacina = ' '.join([x for x in message.text.split()[1:]]).rstrip().lower()
    bot.reply_to(message, procura_vacina(vacina), parse_mode='HTML')

# Inicia o bot a partir de qualquer mensagem

@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def start_natural(message):
    user_id = message.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {"started_once": True}
        start(message)
    else:
        bot.reply_to(message, 'Use: /start para exibir o menu novamente')

# Callbacks - editam a primeira mensagem e retornar a vacina de acordo com a situação
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    def edita_mensagem(mensagem):
        bot.edit_message_text(pega_vacina(mensagem), call.message.chat.id, call.message.message_id, parse_mode='HTML')

    if call.data.endswith('gestante'):
        edita_mensagem('Gestante')

    if call.data.endswith('crianca'):
        edita_mensagem('Criança')

    if call.data.endswith('adolescente'):
        edita_mensagem('Adolescente')
    
    if call.data.endswith('adulto'):
        edita_mensagem('Adulto')
    
    if call.data.endswith('idoso'):
        edita_mensagem('Idoso')

    # Exibe o menu novamente após a exibição das vacinas

    bot.answer_callback_query(call.id)

# Iniciar bot
bot.polling()
