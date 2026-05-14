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

TOKEN = "8513074082:AAEdhwh-BRONRAuKDZmNzHILG-kwdWJYtbE"
bot = telebot.TeleBot(TOKEN)

user_data = {}
ultimo_clique = {}
reiniciar_menu_natural = timedelta(minutes=1)
pdf_cooldown = {}
COOLDOWN_PDF = 5

grupos = {
    'grupo_gestante': 'Gestante',
    'grupo_crianca': 'Criança',
    'grupo_jovens': 'Adolescente',
    'grupo_adulto': 'Adulto',
    'grupo_idoso': 'Idoso'
}

regioes = {
    'norte': 'Norte',
    'nordeste': 'Nordeste',
    'centrooeste': 'Centro-Oeste',
    'sudeste': 'Sudeste',
    'sul': 'Sul'
}

def anti_spam(user_id, action, cooldown=0.8):
    key = f'{user_id}:{action}'
    now = time.time()
    if key in ultimo_clique and now - ultimo_clique[key] < cooldown:
        return False
    ultimo_clique[key] = now
    return True


def delete_if_exists(chat_id, user_id, key):
    data = user_data.get(user_id, {})
    if not data:
        return
    
    msg_id = data.get(key)
    if not msg_id:
        return

    try:
        bot.delete_message(chat_id, msg_id)
    except:
        pass
    
    data[key] = None


def save_msg_id(user_id, key, msg):
    user_data.setdefault(user_id, {})[key] = msg.message_id


def safe_edit(text, chat_id, message_id, markup=None):
    try:
        bot.edit_message_text(
            text,
            chat_id,
            message_id,
            reply_markup=markup,
            parse_mode='HTML'
        )
    except Exception:
        pass

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
    chat_id = message.chat.id
    data = user_data.setdefault(user_id, {})
    old_msg_id = data.get('menu_msg_id')
    
    for key in ['menu_msg_id', 'warning_msg_id', 'pdf_msg_id', 'search_msg_id']:
        delete_if_exists(chat_id, user_id, key)

    data['ultimo_menu'] = datetime.now()
    menu(chat_id, user_id)

# Menu principal
def menu_principal():
    return quick_markup({
        'Calendário Vacinal 📅': {'callback_data': 'calendario_vacinal'},
        'Cobertura 📊': {'callback_data': 'cobertura'},
        'Assistente IA 🤖': {'callback_data': 'assistente'},
        'Localizar 📍': {'callback_data': 'localizar'},
        'Saiba Mais ℹ️': {'callback_data': 'fontes'},
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
    except Exception:
        pass

# Função que envia ou edita o menu
def menu(chat_id, user_id):
    text = 'Bem-vindo(a) ao Vacina Brasil Bot 💉🇧🇷\nO que deseja consultar hoje?'
    markup = menu_principal()
    
    data = user_data.setdefault(user_id, {})
    old_msg_id = data.get('menu_msg_id')
    
    if old_msg_id:
        try:
            bot.delete_message(chat_id, old_msg_id)
        except:
            pass
        
    old_warning = data.get('warning_msg_id')
    
    if old_warning:
        try:
            bot.delete_message(chat_id, old_warning)
        except:
            pass
            
    msg = bot.send_message(chat_id, text, reply_markup=markup)
    data['menu_msg_id'] = msg.message_id

# /procurar
@bot.message_handler(commands=['procurar'])
def procurar(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    data = user_data.setdefault(user_id, {})

    delete_if_exists(chat_id, user_id, 'search_msg_id')
    
    if len(message.text.split()) < 2:
        msg = bot.reply_to(message, 'Use: /procurar nome da vacina ou região.')
        save_msg_id(user_id, 'search_msg_id', msg)
        return
    termo = ' '.join(message.text.split()[1:]).strip().lower()
    termo_regiao = termo.replace('-', '').replace(' ', '')
    regioes = {'norte': 'Norte', 'nordeste': 'Nordeste',  'centrooeste': 'Centro-Oeste', 'sudeste': 'Sudeste', 'sul': 'Sul'}
    
    if termo_regiao in regioes:
        msg = bot.reply_to(message, consultar_cobertura(regioes[termo_regiao]))
        save_msg_id(user_id, 'search_msg_id', msg)
        return
    
    resposta = procura_vacina(termo)
    msg = bot.reply_to(message, resposta, parse_mode='HTML')
    save_msg_id(user_id, 'search_msg_id', msg)

# Inicia o bot a partir de qualquer mensagem
@bot.message_handler(func=lambda m: m.text and not m.text.startswith('/'))
def start_natural(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    agora = datetime.now()
    
    data = user_data.setdefault(user_id, {})
    
    ultimo_menu = data.get('ultimo_menu')
    
    if ultimo_menu is None:
        data['ultimo_menu'] = agora
        menu(chat_id, user_id)
        return

    if agora - ultimo_menu >= reiniciar_menu_natural:
        data['ultimo_menu'] = agora
        delete_if_exists(chat_id, user_id, 'pdf_msg_id')
        delete_if_exists(chat_id, user_id, 'search_msg_id')
        menu(chat_id, user_id)
    else:
        msg = bot.reply_to(message, 'Use: /start para exibir o menu novamente ou aguarde um minuto.')
        save_msg_id(user_id, 'search_msg_id', msg)

# Função pra voltar
def volta_para(call, destino):
    menus = {
        'menu_principal': ('Bem-vindo(a) ao Vacina Brasil Bot 💉🇧🇷\nO que deseja consultar hoje?', menu_principal),
        'calendario_vacinal': ('Escolha a faixa etária:', menu_calendario),
        'cobertura': ('Escolha a região:', menu_regioes),
    }
    if destino in menus:
        texto, menu_func = menus[destino]
        safe_edit(texto, call.message.chat.id, call.message.message_id, menu_func())

# Callbacks
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    
    user_id = call.from_user.id
    
    data = user_data.get(user_id, {})
    
    if not anti_spam(user_id, call.data):
        return
    
    valid_ids = [
        data.get('menu_msg_id'),
        data.get('pdf_msg_id')
    ]
    
    if call.message.message_id not in valid_ids:
        try:
            bot.answer_callback_query(call.id)
        except:
            pass
        return

    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass

    def edita_mensagem(mensagem, grupo):
        
        texto2 = pega_vacina(mensagem)
        
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton('📄 Ver ou Baixar PDF', callback_data=f'baixar_pdf_{grupo}'))
        
        markup.row(InlineKeyboardButton('⬅️ Voltar', callback_data='voltar_calendario'))
        
        safe_edit(texto2, call.message.chat.id, call.message.message_id, markup)

    if call.data == 'calendario_vacinal':
        safe_edit('Escolha a faixa etária:', call.message.chat.id, call.message.message_id, menu_calendario())
    
    elif call.data.startswith('baixar_pdf_'):

        user_id = call.from_user.id
        data = user_data.setdefault(user_id, {})
        now = time.time()
        
        if data.get('pdf_msg_id'):
            bot.answer_callback_query(call.id, "📄 O PDF já está aberto")
            return
        
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
        
        delete_if_exists(
            call.message.chat.id,
            user_id,
            'pdf_msg_id'
        )

        msg_pdf = bot.send_message(call.message.chat.id,
            f'📄 Calendário de vacinação - {nome}\n\n'
            f'🔗 <a href="{url}">Abrir documento oficial (PDF)</a>\n\n', parse_mode='HTML')

        data['pdf_msg_id'] = msg_pdf.message_id

    elif call.data == 'cobertura':
        safe_edit('Escolha a região:', call.message.chat.id, call.message.message_id, menu_regioes())

    elif call.data.startswith('regiao_'):
        regiao = call.data.replace('regiao_', '')
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton('⬅️ Voltar', callback_data='voltar_cobertura'))
        safe_edit(consultar_cobertura(regiao), call.message.chat.id, call.message.message_id, markup)
        
    elif call.data == 'fontes':
        
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton('⬅️ Voltar', callback_data='voltar_menu'))
    
        safe_edit(
            'ℹ️ <b>Fontes oficiais do sistema</b>\n\n'
            
            '📄 <b>Calendários de Vacinação (PDFs)</b>\n\u200B \n'
            'https://www.gov.br/saude/pt-br/vacinacao/arquivos/\n\n'
            
            '📊 <b>Dados da Cobertura Vacinal</b>\n\u200B \n'
            'https://infoms.saude.gov.br/extensions/SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA/SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA.html\n\n'
            
            '👨‍💻 <b>Sobre o Bot</b>\n\u200B \n'
            '<b>Assistente virtual para Telegram que informa vacinas recomendadas com base na faixa etária.</b>\n\n'
            'Projeto desenvolvido durante o <b>1º semestre de 2026</b> por estudantes do curso de <b>Análise e Desenvolvimento de Sistemas</b> da <b>FATEC São José dos Campos.</b>\n\n'
            'O projeto segue a metodologia ágil <b>Scrum</b>, com foco em <b>desenvolvimento colaborativo e organização de tarefas.</b>\n\n'
            
            '👥 <b>Equipe</b>\n\u200B \n'
            '• Nicolas Fonseca Meira — Scrum Master\n'
            '• Miguel Silva Gomes — Product Owner\n'
            '• Gabriel Yudi Fujimoto — Scrum Team\n',
            call.message.chat.id,
            call.message.message_id,
            markup
        )

    # Botões de voltar
    if call.data == 'voltar_menu':
        volta_para(call, 'menu_principal')

    elif call.data == 'voltar_calendario':
        try:
            bot.answer_callback_query(call.id)
        except:
            pass

        safe_edit(
            'Escolha a faixa etária:',
            call.message.chat.id,
            call.message.message_id,
            menu_calendario()
        )
        
        delete_if_exists(
            call.message.chat.id,
            user_id,
            'pdf_msg_id'
        )

    elif call.data == 'voltar_cobertura':
        safe_edit(
            'Escolha a região:',
            call.message.chat.id,
            call.message.message_id,
            menu_regioes()
        )

    elif call.data in grupos:
        edita_mensagem(grupos[call.data], call.data)

    elif call.data == 'calendario_vacinal':
        safe_edit(
            'Escolha a faixa etária:',
            call.message.chat.id,
            call.message.message_id,
            menu_calendario()
        )

    elif call.data == 'cobertura':
        safe_edit(
            'Escolha a região:',
            call.message.chat.id,
            call.message.message_id,
            menu_regioes()
        )

    bot.answer_callback_query(call.id)

# Verifica se há alguma atualização nos calendários
se_precisar_update()
# Iniciar bot
bot.polling()