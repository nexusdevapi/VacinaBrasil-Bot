import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup
from datetime import datetime, timedelta
from core.engine import *
from data_handler.scraping_update import se_precisar_update
import json
from pathlib import Path

TOKEN = ""
bot = telebot.TeleBot(TOKEN)

user_data = {}

reiniciar_menu_natural = timedelta(minutes=1)

JSON_COBERTURA = Path("src/data/processed/cobertura_vacinal.json")

# Consultar cobertura vacinal
def consultar_cobertura(regiao):
    with open(JSON_COBERTURA, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if regiao not in dados:
        return "Região não encontrada!"

    info = dados[regiao]

    texto = f"📊 Cobertura vacinal - {regiao}\n\n"
    texto += f"Cobertura geral: {info['cobertura_geral']}%\n\n"
    texto += "Vacinas:\n\n"

    for vacina, cobertura in info["vacinas"].items():
        texto += f"- {vacina}: {cobertura}%\n"

    return texto

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

    def edita_mensagem(mensagem):
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("⬅️ Voltar", callback_data="voltar"))
        bot.edit_message_text(pega_vacina(mensagem), call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)

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

        bot.edit_message_text("Escolha a região:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    if call.data.startswith('regiao_'):
        regiao = call.data.replace('regiao_', '')

        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("⬅️ Voltar", callback_data="voltar"))

        bot.edit_message_text(
            consultar_cobertura(regiao),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    if call.data == 'voltar':
        markup = quick_markup({
            'Gestante 🤰': {'callback_data': 'grupo_gestante'},
            'Criança 👶': {'callback_data': 'grupo_crianca'},
            'Jovens 🧑': {'callback_data': 'grupo_adolescente'},
            'Adulto 🧑‍💼': {'callback_data': 'grupo_adulto'},
            'Idoso 👴': {'callback_data': 'grupo_idoso'},
            'Cobertura 📊': {'callback_data': 'cobertura'}
        }, row_width=3)
    
        bot.edit_message_text("Bem-vindo(a) ao Vacina Brasil Bot 💉🇧🇷\nEscolha o que deseja consultar:", call.message.chat.id, call.message.message_id, reply_markup=markup)

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

# Verifica se há alguma atualização nos calendários
se_precisar_update()
# Iniciar bot
bot.polling()