import re
from data_handler.loader import *

def pega_vacina(periodo):
    resultado = ''
    data = carregar_json('calendario_vacinas.json')
    data = [info for info in data if info['grupo'].split()[0] == periodo]

    for info in data:
        if info['idade_texto'] != '':
            resultado += f'<b>{info['idade_texto'].replace('\n', ' ')}</b>\n' if resultado == '' else f'\n<b>{info['idade_texto'].replace('\n', ' ')}</b>\n'
        resultado += f'{info['vacina'].replace('\n', ' ')}\n    - {info['dose'].replace('\n', ' ')}\n'
    return resultado

def procura_vacina(nome):
    status = ''
    resultado = ''
    data = carregar_json('calendario_vacinas.json')
    nome = nome.lower().strip()
    for info in data:
        if info['idade_texto'] != '':
            status = info['idade_texto']
        vacina = re.sub(r'\d+|[¹²³⁴⁵⁶⁷⁸⁹]', '', info['vacina'])
        vacina = vacina.replace('\n', ' ').lower().strip()
        if vacina == nome or (nome != 'dt' and vacina.startswith(nome + ' ')):
            resultado += f'<b>{status.replace('\n', ' ')}</b>\n' if resultado == '' else f'\n<b>{status.replace('\n', ' ')}</b>\n'
            resultado += f'{info['vacina'].replace('\n', ' ')}\n    - {info['dose'].replace('\n', ' ')}\n'
    if resultado == '':
        resultado = 'Vacina não encontrada!'
    return resultado