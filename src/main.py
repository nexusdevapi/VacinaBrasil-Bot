import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup
from datetime import datetime, timedelta
from core.engine import *
from data_handler.scraping_update import se_precisar_update
import time
import json
from pathlib import Path

TOKEN = "8513074082:AAGjP_NN8H8EuLWU1xwzRBRQ7ycSwlw--j0"
bot = telebot.TeleBot(TOKEN)

user_data = {}

ultimo_clique = {}

reiniciar_menu_natural = timedelta(minutes=1)

# Evita spam de botões
def anti_spam(user_id, action, cooldown=0.8):
    key = f"{user_id}:{action}"
    now = time.time()

    if key in ultimo_clique and now - ultimo_clique[key] < cooldown:
        return False

    ultimo_clique[key] = now
    return True

# /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    user_data[user_id] = {"ultimo_menu": datetime.now()}

    menu(message.chat.id)

# Cria botões inline para escolha da faixa etária/grupo
def menu(chat_id):
    markup = quick_markup({
        'Gestante 🤰': {'callback_data': 'grupo_gestante'},
        'Criança 👶': {'callback_data': 'grupo_crianca'},
        'Jovens 🧑': {'callback_data': 'grupo_adolescente'},
        'Adulto 🧑‍💼': {'callback_data': 'grupo_adulto'},
        'Idoso 👴': {'callback_data': 'grupo_idoso'},
        'Cobertura 📊': {'callback_data': 'cobertura'}
    }, row_width=3)
    
    bot.send_message(chat_id, "Bem-vindo(a) ao Vacina Brasil Bot 💉🇧🇷\nEscolha o que deseja consultar:", reply_markup=markup)
    
# Evita spam de botões
def safe_edit(text, chat_id, message_id, markup=None):
    try:
        bot.edit_message_text(
            text,
            chat_id,
            message_id,
            reply_markup=markup,
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"[safe_edit erro] {e}")

# /procurar
@bot.message_handler(commands=['procurar'])
def procurar(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Use: /procurar nome da vacina ou região.')
        return

    termo = ' '.join(message.text.split()[1:]).strip().lower()

    termo_regiao = termo.replace("-", "").replace(" ", "")

    regioes = {"norte": "Norte", "nordeste": "Nordeste",  "centrooeste": "Centro-Oeste", "sudeste": "Sudeste", "sul": "Sul"}

    if termo_regiao in regioes:
        return bot.reply_to(message, consultar_cobertura(regioes[termo_regiao]))

    resposta = procura_vacina(termo)

    bot.reply_to(message, resposta, parse_mode='HTML')

# Inicia o bot a partir de qualquer mensagem
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def start_natural(message):
    user_id = message.from_user.id

    agora = datetime.now()

    if user_id not in user_data:
        user_data[user_id] = {"ultimo_menu": agora}
        menu(message.chat.id)
        return

    ultimo_menu = user_data[user_id]["ultimo_menu"]

    if agora - ultimo_menu >= reiniciar_menu_natural:
        user_data[user_id]["ultimo_menu"] = agora
        menu(message.chat.id)
    else:
        bot.reply_to(message, 'Use: /start para exibir o menu novamente ou aguarde um minuto.')

# Callbacks
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    
    user_id = call.from_user.id

    if not anti_spam(user_id, call.data):
        bot.answer_callback_query(call.id)
        return

    def edita_mensagem(mensagem):
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("⬅️ Voltar", callback_data="voltar"))
        try:
            safe_edit(pega_vacina(mensagem), call.message.chat.id, call.message.message_id, markup)
        except Exception:
            pass

    if call.data == 'cobertura':
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton("Norte", callback_data="regiao_Norte"),
            InlineKeyboardButton("Nordeste", callback_data="regiao_Nordeste")
        )

        markup.row(
            InlineKeyboardButton("Centro-Oeste", callback_data="regiao_Centro-Oeste"),
            InlineKeyboardButton("Sudeste", callback_data="regiao_Sudeste")
        )

        markup.row(
            InlineKeyboardButton("Sul", callback_data="regiao_Sul")
        )

        markup.row(
            InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")
        )

        safe_edit("Escolha a região:", call.message.chat.id, call.message.message_id, markup)

    elif call.data.startswith('regiao_'):
        regiao = call.data.replace('regiao_', '')

        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("⬅️ Voltar", callback_data="voltar"))

        safe_edit(consultar_cobertura(regiao), call.message.chat.id, call.message.message_id, markup)

    elif call.data == 'voltar':
        markup = quick_markup({
            'Gestante 🤰': {'callback_data': 'grupo_gestante'},
            'Criança 👶': {'callback_data': 'grupo_crianca'},
            'Jovens 🧑': {'callback_data': 'grupo_adolescente'},
            'Adulto 🧑‍💼': {'callback_data': 'grupo_adulto'},
            'Idoso 👴': {'callback_data': 'grupo_idoso'},
            'Cobertura 📊': {'callback_data': 'cobertura'}
        }, row_width=3)
    
        safe_edit("Bem-vindo(a) ao Vacina Brasil Bot 💉🇧🇷\nEscolha o que deseja consultar:", call.message.chat.id, call.message.message_id, markup)

    elif call.data.endswith('gestante'):
        edita_mensagem('Gestante')

    elif call.data.endswith('crianca'):
        edita_mensagem('Criança')

    elif call.data.endswith('adolescente'):
        edita_mensagem('Adolescente')
    
    elif call.data.endswith('adulto'):
        edita_mensagem('Adulto')
    
    elif call.data.endswith('idoso'):
        edita_mensagem('Idoso')

# Verifica se há alguma atualização nos calendários
se_precisar_update()
# Iniciar bot
bot.polling()
