import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup
from datetime import datetime, timedelta
from core.engine import *
from utils.helpers import *
from data_handler.scraping_update import se_precisar_update
import time
import json
import requests
from pathlib import Path
from io import BytesIO

TOKEN = ""
bot = telebot.TeleBot(TOKEN)

user_data = {}
ultimo_clique = {}
reiniciar_menu_natural = timedelta(minutes=1)
pdf_cooldown = {}
COOLDOWN_PDF = 5

# Evita spam de botões
def anti_spam(user_id, action, cooldown=0.8):
    key = f'{user_id}:{action}'
    now = time.time()
    if key in ultimo_clique and now - ultimo_clique[key] < cooldown:
        return False
    ultimo_clique[key] = now
    return True

# /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_data[user_id] = {'ultimo_menu': datetime.now()}
    menu(message.chat.id)

# Menu principal
def menu_principal():
    return quick_markup({
        'Calendário Vacinal 📅': {'callback_data': 'calendario_vacinal'},
        'Cobertura 📊': {'callback_data': 'cobertura'},
        'Fontes ℹ️': {'callback_data': 'fontes'}
    }, row_width=2)

# Menu regiões - cobertura
def menu_regioes():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton('Norte', callback_data='regiao_Norte'),
        InlineKeyboardButton('Nordeste', callback_data='regiao_Nordeste')
    )
    markup.row(
        InlineKeyboardButton('Centro-Oeste', callback_data='regiao_Centro-Oeste'),
        InlineKeyboardButton('Sudeste', callback_data='regiao_Sudeste')
    )
    markup.row(
        InlineKeyboardButton('Sul', callback_data='regiao_Sul')
    )
    markup.row(
        InlineKeyboardButton('⬅️ Voltar', callback_data='voltar_menu')
    )
    return markup

# Cria botões dentro da faixa etária para escolha
def menu_calendario():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton('Gestante 🤰', callback_data='grupo_gestante'),
        InlineKeyboardButton('Criança 👶', callback_data='grupo_crianca'),
        InlineKeyboardButton('Jovens 🧑', callback_data='grupo_jovens')
    )
    markup.row(
        InlineKeyboardButton('Adulto 🧑‍💼', callback_data='grupo_adulto'),
        InlineKeyboardButton('Idoso 👴', callback_data='grupo_idoso')
    )
    markup.row(
        InlineKeyboardButton('⬅️ Voltar', callback_data='voltar_menu')
    )
    return markup

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
        print(f'[safe_edit erro] {e}')

# Função que envia ou edita o menu
def menu(chat_id, message_id=None):
    text = 'Bem-vindo(a) ao Vacina Brasil Bot 💉🇧🇷\nO que deseja consultar hoje?'
    markup = menu_principal()
    if message_id:
        safe_edit(text, chat_id, message_id, markup)
    else:
        bot.send_message(chat_id, text, reply_markup=markup)        

# /procurar
@bot.message_handler(commands=['procurar'])
def procurar(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Use: /procurar nome da vacina ou região.')
        return
    termo = ' '.join(message.text.split()[1:]).strip().lower()
    termo_regiao = termo.replace('-', '').replace(' ', '')
    regioes = {'norte': 'Norte', 'nordeste': 'Nordeste',  'centrooeste': 'Centro-Oeste', 'sudeste': 'Sudeste', 'sul': 'Sul'}
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
        user_data[user_id] = {'ultimo_menu': agora}
        menu(message.chat.id)
        return
    ultimo_menu = user_data[user_id]['ultimo_menu']
    if agora - ultimo_menu >= reiniciar_menu_natural:
        user_data[user_id]['ultimo_menu'] = agora
        menu(message.chat.id)
    else:
        bot.reply_to(message, 'Use: /start para exibir o menu novamente ou aguarde um minuto.')

# Função pra voltar
def volta_para(call, destino):
    menus = {
        'menu_principal': ('Bem-vindo(a) ao Vacina Brasil Bot 💉🇧🇷\nO que deseja consultar hoje?', menu_principal),
        'calendario': ('Escolha a faixa etária:', menu_calendario),
        'cobertura': ('Escolha a região:', menu_regioes),
    }
    if destino in menus:
        texto, menu_func = menus[destino]
        safe_edit(texto, call.message.chat.id, call.message.message_id, menu_func())

# Callbacks
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    if not anti_spam(user_id, call.data):
        bot.answer_callback_query(call.id)
        return

    def edita_mensagem(mensagem, grupo):
        
        texto2 = pega_vacina(mensagem)
        
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton('📄 Ver ou Baixar PDF', callback_data=f'baixar_pdf_{grupo}'))
        
        markup.row(InlineKeyboardButton('⬅️ Voltar', callback_data='voltar_calendario'))
        
        try:
            safe_edit(texto2, call.message.chat.id, call.message.message_id, markup)
        except Exception:
            pass

    if call.data == 'calendario_vacinal':
        safe_edit('Escolha a faixa etária:', call.message.chat.id, call.message.message_id, menu_calendario())
    
    elif call.data.startswith('baixar_pdf_'):

        user_id = call.from_user.id
        now = time.time()
        
        if user_id in pdf_cooldown:
            if now - pdf_cooldown[user_id] < COOLDOWN_PDF:
                bot.answer_callback_query(
                    call.id,
                    '⏳ Aguarde um pouco antes de baixar novamente'
                )
                return
        
        pdf_cooldown[user_id] = now
        
        grupo = call.data.replace('baixar_pdf_', '')

        url = urls.get(grupo)

        if not url:
            bot.answer_callback_query(call.id, 'PDF não encontrado')
            return

        nome = grupo.replace('grupo_', '').capitalize()

        msg_pdf = bot.send_message(
            call.message.chat.id,
            '📄 Calendário de vacinação - ' + nome + '\n\n'
            '🔗 <a href='' + url + ''>Abrir documento oficial (PDF)</a>\n\n',
            parse_mode='HTML',
            disable_web_page_preview=False
        )

        user_data.setdefault(call.from_user.id, {})['pdf_msg_id'] = msg_pdf.message_id

    elif call.data == 'cobertura':
        safe_edit('Escolha a região:', call.message.chat.id, call.message.message_id, menu_regioes())

    elif call.data.startswith('regiao_'):
        regiao = call.data.replace('regiao_', '')
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton('⬅️ Voltar', callback_data='voltar_cobertura'))
        safe_edit(consultar_cobertura(regiao), call.message.chat.id, call.message.message_id, markup)
        
    elif call.data == 'fontes':
        safe_edit(
            'ℹ️ <b>Fontes oficiais do sistema</b>\n\n'
            '📄 <b>Calendário vacinal (PDFs)</b>\n'
            'https://www.gov.br/saude/pt-br/vacinacao/arquivos/\n\n',
            call.message.chat.id,
            call.message.message_id
        )

    elif call.data == 'grupo_gestante':
        edita_mensagem('Gestante', 'grupo_gestante')
    elif call.data == 'grupo_crianca':
        edita_mensagem('Criança', 'grupo_crianca')
    elif call.data == 'grupo_jovens':
        edita_mensagem('Adolescente', 'grupo_jovens')
    elif call.data == 'grupo_adulto':
        edita_mensagem('Adulto', 'grupo_adulto')
    elif call.data == 'grupo_idoso' :
        edita_mensagem('Idoso', 'grupo_idoso')

    # Botões de voltar
    if call.data == 'voltar_menu':
        volta_para(call, 'menu_principal')
    
    elif call.data == 'voltar_calendario':

        user_id = call.from_user.id
        chat_id = call.message.chat.id

        data = user_data.get(user_id, {})

        pdf_id = data.get('pdf_msg_id')

        if pdf_id:
            try:
                bot.delete_message(chat_id, pdf_id)
            except Exception as e:
                print('erro ao deletar pdf:', e)

            data['pdf_msg_id'] = None
            user_data[user_id] = data

        volta_para(call, 'calendario')
    
    elif call.data == 'voltar_cobertura':
        volta_para(call, 'cobertura')
        
    bot.answer_callback_query(call.id)

# Verifica se há alguma atualização nos calendários
se_precisar_update()
# Iniciar bot
bot.polling()