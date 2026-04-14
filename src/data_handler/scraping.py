import json
import re
from io import BytesIO

import requests
import pdfplumber

# obtendo números da faixa etária
def extrair_idade(idade_texto):
    if not idade_texto:
        return None, None

    idade_texto = str(idade_texto).lower()

    if 'ao nascer' in idade_texto:
        return 0, 0

    numeros = re.findall(r'\d+', idade_texto)

    if len(numeros) >= 2:
        return int(numeros[0]), int(numeros[1])
    elif len(numeros) == 1:
        return int(numeros[0]), None
    else:
        return None, None

# calendários relevantes disponíveis em https://www.gov.br/saude/pt-br/vacinacao/arquivos/
urls = [
    'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-idoso/',
    'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-adulto/',
    'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-adolescentes-jovens/',
    'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-crianca/',
    'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-gestante/',
]

# lista que armazena os dados obtidos
arquivo_json = []

for url in urls:
    nome = url.split('/')[-2] + '.pdf'

    if 'idoso' in nome:
        grupo = 'Idoso'
    elif 'adulto' in nome:
        grupo = 'Adulto'
    elif 'adolescentes-jovens' in nome:
        grupo = 'Adolescente e Jovem'
    elif 'crianca' in nome:
        grupo = 'Criança'
    elif 'gestante' in nome:
        grupo = 'Gestante'
    else:
        grupo = 'Nenhum'

    resp = requests.get(url)
    resp.raise_for_status()

    with pdfplumber.open(BytesIO(resp.content)) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()

            if not tabelas:
                continue

            for tabela in tabelas:
                for linha in tabela[1:]:
                    if not linha or len(linha) < 4:
                        continue

                    idade_texto = linha[0] or ''
                    idade_min, idade_max = extrair_idade(idade_texto)

                    registro = {
                        'grupo': grupo,
                        'idade_min': idade_min,
                        'idade_max': idade_max,
                        'idade_texto': idade_texto,
                        'vacina': linha[1] or '',
                        'dose': linha[2] or '',
                        'descricao': linha[3] or '',
                        'observacoes': None
                    }

                    arquivo_json.append(registro)

# salva registros em um arquivo json na pasta "processed"
with open('../data/processed/calendario_vacinas.json', 'w', encoding='utf-8') as f:
    json.dump(arquivo_json, f, ensure_ascii=False, indent=2)
    




