import re
import ollama
import json
import unicodedata
from data_handler.loader import *

def pega_vacina(periodo):
    resultado = ''
    data = carregar_json('calendario_vacinas.json')
    data = [info for info in data if info['grupo'].split()[0] == periodo.split('_')[0]]

    if periodo.endswith('json'):
        return data

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
            resultado += f'🗓️ <b>{status.replace(chr(10), " ")}</b>:\n\n' if resultado == '' else f'🗓️ <b>{status.replace(chr(10), " ")}</b>:\n\n'
            resultado += f'💉 {info["vacina"].replace(chr(10), " ")}\n    • {info["dose"].replace(chr(10), " ")}\n\n'
    if resultado == '':
        resultado = 'Termo não encontrado!'
    return resultado

def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = texto.replace(" ", "").replace("-", "")
    return texto

def consultar_cobertura(local=None, uf=None):
    cobertura = carregar_json(
        'cobertura_vacinal.json'
    )["cobertura_vacinal_geral"]["Brasil"]

    if local is None:
        return list(cobertura.keys())
    
    if local:
        local = normalizar(local)

    for regiao, estados in cobertura.items():
        if normalizar(regiao) == local:
            soma, total = {}, {}
            for estado in estados.values():
                for macro in estado.values():
                    for vacina, vals in macro.get("Totais", {}).items():
                        if vacina == "Município Residência":
                            continue
                        try:
                            if isinstance(vals, dict):
                                soma[vacina] = soma.get(vacina, 0) + vals["num"]
                                total[vacina] = total.get(vacina, 0) + vals["den"]
                            else:
                                soma[vacina] = soma.get(vacina, 0) + float(vals)
                                total[vacina] = total.get(vacina, 0) + 1
                        except:
                            pass
            return formatar_cobertura(f"Região {regiao}", soma, total)

    for regiao, estados in cobertura.items():
        if local.upper() in estados:
            soma, total = {}, {}
            for macro in estados[local.upper()].values():
                for vacina, vals in macro.get("Totais", {}).items():
                    if vacina == "Município Residência":
                        continue
                    try:
                        if isinstance(vals, dict):
                            soma[vacina] = soma.get(vacina, 0) + vals["num"]
                            total[vacina] = total.get(vacina, 0) + vals["den"]
                        else:
                            soma[vacina] = soma.get(vacina, 0) + float(vals)
                            total[vacina] = total.get(vacina, 0) + 1
                    except:
                        pass
            return formatar_cobertura(local.upper(), soma, total)

    for regiao, estados in cobertura.items():
        for uf_estado, macros in estados.items():
            if uf and uf.upper() != uf_estado.upper():
                continue
            for macro in macros.values():
                for codigo, dados_municipio in macro.items():
                    if codigo == "Totais":
                        continue
                    municipio = dados_municipio.get("Município Residência", "")
                    nome_municipio = municipio.split(" - ")[-1]
                    if normalizar(nome_municipio) == local:
                        soma, total = {}, {}
                        for vacina, vals in dados_municipio.items():
                            if vacina == "Município Residência":
                                continue
                            try:
                                if isinstance(vals, dict):
                                    soma[vacina] = vals["num"] / vals["den"]
                                    total[vacina] = 1
                                else:
                                    soma[vacina] = float(vals)
                                    total[vacina] = 1
                            except:
                                pass
                        return formatar_cobertura(
                            f"{nome_municipio} ({uf_estado})",
                            soma,
                            total
                        )

    return "Local não encontrado."

nomes_estados = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins"
}

def formatar_cobertura(nome, soma, total):
    nome = nomes_estados.get(nome, nome)

    medias = {
        v: round((soma[v] / total[v]) * 100, 2)
        for v in soma
    }

    if not medias:
        return f"📊 <b>Cobertura vacinal</b>\n\n❌ Nenhum dado encontrado para esta região."

    geral = round(sum(soma[v] / total[v] * 100 for v in soma) / len(soma), 2)

    mensagem = (
        f"📊 <b>Cobertura vacinal - {nome}</b>\n\n"
        f"📈 <b>Média das vacinas:</b> {geral}%\n\n"
        f"💉 <b>Vacinas:</b>\n\n"
    )

    for vacina, media in sorted(medias.items()):
        vacina = vacina.replace("<", "&lt;").replace(">", "&gt;")
        mensagem += f"• {vacina}: {media}%\n"

    return mensagem[:3900]

def resto(texto):
    return 'Olá, não entendi sua pergunta. Poderia fazê-lá novamente?'

def dia(nascimento):
    try:
        dia, mes, ano = map(int, nascimento.split('/'))
        nasc = date(ano, mes, dia)
        atual = date.today()
        ano = 0

        if atual.year == nasc.year:
            mes = atual.month - nasc.month
            return idade(f'{mes} months')
        else:
            ano = atual.year - nasc.year

        if not (nasc.month, nasc.day) < (atual.month, atual.day) and ano != 0:
            ano -= 1

        return idade(f'{ano} years')
    except Exception as e:
        return e
   
def idade(id):
    ano = mes = semana = -1
    resultado = ''
    max = mini = 0
    if 'semana' in id or 'week' in id:
        if id == 'semana':
            semana = 1
        semana = int(id.split()[0])
    elif 'month' in id:
        mes = int(id.split()[0])
    elif 'year' in id:
        ano = int(id.split()[0])
        if ano == 1:
            ano = -1
            mes = 12
    
    if semana != -1:
        periodo = 'Gestante_json'
    elif 0 <= ano <= 9 or 0 <= mes <= 15:
        periodo = 'Criança_json'
    elif 10 <= ano <= 24:
        periodo = 'Adolescente_json'
    elif 25 <= ano <= 29:
        return pega_vacina('Adulto')
    elif ano >= 60:
        return pega_vacina('Idoso')

    data = pega_vacina(periodo)

    for info in data:
        if info['idade_min'] is not None:
            mini = info["idade_min"]

        if info['idade_max'] is not None:
            max = info["idade_max"]

        if info['idade_min'] is None:
            info['idade_min'] = mini

        if info['idade_max'] is None:
            info["idade_max"] =  max

        if semana != -1 and ano == mes == -1:
            match = re.search(r'(\d+)ª', info['dose'])
            if match and semana < int(match.group(1)):
                return resultado
            if info['idade_texto'] != '':
                resultado += f'🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n' if resultado == '' else f'───────────────────\n\n🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n'
            resultado += f'💉 {info['vacina'].replace('\n', ' ')}\n    • {info['dose'].replace('\n', ' ')}\n\n'
        elif mes == 0 and ano == 0:
            if info['idade_min'] == info['idade_max'] == 0:
                if info['idade_texto'] != '':
                    resultado += f'🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n'
                resultado += f'💉 {info['vacina'].replace('\n', ' ')}\n    • {info['dose'].replace('\n', ' ')}\n\n'
        elif mes > 0 and ano == 0:
            if info['idade_texto'].endswith('anos'):
                return resultado

            if info['idade_max'] is None:
                if mes >= info['idade_min']:
                    if info['idade_texto'] != '':
                        resultado += f'🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n' if resultado == '' else f'───────────────────\n\n🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n'
                    resultado += f'💉 {info['vacina'].replace('\n', ' ')}\n    • {info['dose'].replace('\n', ' ')}\n\n'
            else:
                if info['idade_min'] <= mes <= info['idade_max'] or mes >= info['idade_min']:
                    if info['idade_texto'] != '':
                        resultado += f'🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n' if resultado == '' else f'───────────────────\n\n🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n'
                    resultado += f'💉 {info['vacina'].replace('\n', ' ')}\n    • {info['dose'].replace('\n', ' ')}\n\n'
        else:
            if info['idade_texto'].endswith('meses'):
                continue

            if info['idade_max'] is None:
                if ano >= info['idade_min']:
                    if info['idade_texto'] != '':
                        resultado += f'🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n' if resultado == '' else f'───────────────────\n\n🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n'
                    resultado += f'💉 {info['vacina'].replace('\n', ' ')}\n    • {info['dose'].replace('\n', ' ')}\n\n'
            else:
                if info['idade_min'] <= ano <= info['idade_max']:
                    if info['idade_texto'] != '':
                        resultado += f'🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n' if resultado == '' else f'───────────────────\n\n🗓️ <b>{info['idade_texto'].replace('\n', ' ')}</b>:\n\n'
                    resultado += f'💉 {info['vacina'].replace('\n', ' ')}\n    • {info['dose'].replace('\n', ' ')}\n\n'
    return resultado

def resposta_ia(perg):
    functions = {
        "pega": pega_vacina,
        "procura": procura_vacina,
        "cobertura": consultar_cobertura,
        "dia": dia,
        "idade": idade,
        "resto": resto
    }

    prompt = f"""
    You are a function selector.

    Available functions:
    - pega: searchs vaccine for age groups like child, adult or elderly. choose one of the arguments[Gestante, Criança, Adolescente e Jovem, Adulto, Idoso] accordingly to the age group
    - procura: uses the name of a vaccine for example dengue or hepatite.
    - cobertura: uses the main regions of brazil. arguments[Norte, Nordeste, Centro-Oeste, Sul, Sudeste]
    - dia: transforms a date in this format: dd/mm/yyyy.
    - idade: uses the age of the user and classifies them in one of the three data types(years, months or weeks). For the arguments return a string in this format: x years or y months or z weeks. Don't pick any value resembling a date for this function. If the age passes 99 return 99 years. Keep the same value as the user gave just put a type on them.
    - resto: uses anything unrelated to the other functions.

    for the idade function:
    Dont convert the values. Keep them the same. Change semana to week

    User request:
    "{perg}"

    Reply with a JSON in this format:
    {{
        "funcao": "function_name",
        "args": "arguments"
    }}

    Return only valid JSON.
    Dont use '''
    """
    response = ollama.chat(
        model='qwen2.5',
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )
    selected = response['message']['content'].strip()
    selected = json.loads(selected)

    if selected['funcao'] in functions:
        return functions[selected['funcao']](selected['args'])