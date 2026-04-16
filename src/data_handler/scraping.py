import json
import sys
from io import BytesIO
from pathlib import Path

import requests
import pdfplumber

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from utils.helpers import extrair_idade

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
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_DIR / "calendario_vacinas.json", "w", encoding="utf-8") as f:
    json.dump(arquivo_json, f, ensure_ascii=False, indent=2)
    




