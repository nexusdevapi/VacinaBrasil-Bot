import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup
from datetime import datetime
from core.engine import vacinas
from core.validator import validate

TOKEN = "8266156765:AAGL-xN8VBkcXoXHPk5-_arliCnkRQNRIUA"
bot = telebot.TeleBot(TOKEN)

user_data = {}
idade = 0
# /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_data[user_id] = {}

    # Cria botões inline para escolher caso seja gestante ou não
    markup = quick_markup({
        'Desejo ver as minhas vacinas': {'callback_data': 'vac'},
        'Sou gestante': {'callback_data': 'gestante'}
    }, row_width=1)
    
    bot.send_message(message.chat.id, "Escolha sua opção:", reply_markup=markup)

@bot.message_handler(commands=['procurar'])
def procurar(message):
    if user_data:
        vacina = ''
        if len(message.text.split()) < 2:
            bot.reply_to(message, 'Use: /procurar nome da vacina')
            return
        for m in message.text.split()[1:]:
            vacina += m + ''
        vacina = vacina.rstrip().lower()
        vacina = vacinas(f'{idade}_{vacina}')
        bot.reply_to(message, f'{vacina}')
    else:
        bot.reply_to(message, 'Use: /start antes')
        return

# CALLBACKS
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id

    # Cria botões para escolher o dia do nascimento, inicia uma sequência de mensagens para definir a data de nascimento
    if call.data == "vac":
        markup = InlineKeyboardMarkup(row_width=7)
        buttons = [InlineKeyboardButton(str(i), callback_data=f"dia_{i}") for i in range(1, 32)]
        markup.add(*buttons)
        
        bot.edit_message_text("Escolha o Dia:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # Cria botões para escolher a semana de gestação
    elif call.data == 'gestante':

        markup = InlineKeyboardMarkup(row_width=5)
        buttons = [InlineKeyboardButton(str(i), callback_data=f"semana_{i}") for i in range(1, 41)]
        markup.add(*buttons)

        bot.edit_message_text("Escolha a semana de gestação", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    # retorna as vacinas de acordo com a gestação
    elif call.data.startswith("semana_"):
        vacina = vacinas(call.data)
        bot.edit_message_text(f"{vacina}", call.message.chat.id, call.message.message_id)

    # Dia
    elif call.data.startswith("dia_"):
        dia = int(call.data.split("_")[1])
        user_data[user_id]["dia"] = dia
        
        markup = InlineKeyboardMarkup(row_width=4)
        buttons = [InlineKeyboardButton(str(i), callback_data=f"mes_{i}") for i in range(1, 13)]
        markup.add(*buttons)
        
        bot.edit_message_text("Agora escolha o Mês:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # Mês
    elif call.data.startswith("mes_"):
        mes = int(call.data.split("_")[1])
        user_data[user_id]["mes"] = mes
        
        current_year = datetime.now().year
        
        markup = InlineKeyboardMarkup(row_width=5)
        buttons = [
            InlineKeyboardButton(str(i), callback_data=f"ano_{i}")
            for i in range(current_year, current_year - 100, -1)
        ]
        markup.add(*buttons)
        
        bot.edit_message_text("Agora escolha o Ano:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # Ano
    elif call.data.startswith("ano_"):
        ano = int(call.data.split("_")[1])
        user_data[user_id]["ano"] = ano
        
        idade = validate(user_data[user_id]["dia"], user_data[user_id]["mes"], user_data[user_id]["ano"]) #verifica a idade

        # Reinicia o processo caso a idade seja inválida
        if not idade:
            bot.send_message(call.message.chat.id, "Data inválida! Vamos recomeçar.")
            start(call.message)

        #retorna as vacinas necessárias
        else:
            vacina = vacinas(idade)
            bot.edit_message_text(f"{vacina}", call.message.chat.id, call.message.message_id)
        
# Iniciar bot
bot.polling()