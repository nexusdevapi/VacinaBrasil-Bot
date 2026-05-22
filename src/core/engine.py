import re
import ollama
import json
from data_handler.loader import *

def pega_vacina(periodo):
    resultado = ''
    data = carregar_json('calendario_vacinas.json')
    data = [info for info in data if info['grupo'].split()[0] == periodo]

    for info in data:
        if info['idade_texto'] != '':
            resultado += f'🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n' if resultado == '' else f'───────────────────\n\n🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n'
        resultado += f'💉 {info['vacina'].replace('\n', ' ')}\n    • {info['dose'].replace('\n', ' ')}\n\n'
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
            resultado += f'🗓️ <b>{status.replace('\n', ' ')}</b>:\n\n' if resultado == '' else f'🗓️ <b>{status.replace('\n', ' ')}</b>:\n\n'
            resultado += f'💉 {info['vacina'].replace('\n', ' ')}\n    • {info['dose'].replace('\n', ' ')}\n\n'
    if resultado == '':
        resultado = 'Termo não encontrado!'
    return resultado

# Consultar cobertura vacinal
def consultar_cobertura(regiao):
    dados = carregar_json('cobertura_vacinal.json')

    if regiao not in dados:
        return "Região não encontrada!"

    info = dados[regiao]

    texto = f"📊 Cobertura vacinal - {regiao}\n\n"
    texto += f"Cobertura geral: {info['cobertura_geral']}%\n\n"
    texto += "💉 Vacinas:\n\n"

    for vacina, cobertura in info["vacinas"].items():
        texto += f"• {vacina}: {cobertura}%\n"

    return texto

def resto(texto):
    return 'Olá, não entendi sua pergunta. Poderia fazê-lá novamente?'

#def idade(ano): WIP
    #return f'{ano} anos'
    #- idade: transforms the user request into a date in this format: dd/mm/yyyy.

def resposta_ia(perg):
    functions = {
        "pega": pega_vacina,
        "procura": procura_vacina,
        "cobertura": consultar_cobertura,
        "resto": resto
    }

    prompt = f"""
    You are a function selector.

    Available functions:
    - pega: searchs vaccine for age groups like child, adult or elderly. choose one of the arguments[Gestante, Criança, Adolescente e Jovem, Adulto, Idoso] accordingly to the age group
    - procura: uses the name of a vaccine for example dengue or hepatite.
    - cobertura: uses the main regions of brazil. arguments[Norte, Nordeste, Centro-Oeste, Sul, Sudeste]
    - resto: uses anything unrelated to the other functions.

    User request:
    "{perg}"

    Reply with a JSON in this format:
    {{
        "funcao": "function_name",
        "args": "arguments"
    }}
    """
    response = ollama.chat(
        model='mistral',
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )

    selected = response['message']['content'].strip()
    selected = json.loads(selected)

    if selected['funcao'] in functions:
        return functions[selected['funcao']](selected['args'])