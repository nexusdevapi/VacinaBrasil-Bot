from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[1]

def carregar_json(nome_arquivo):
    caminho = BASE_DIR / "data" / "processed" / nome_arquivo
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
    
def carregar_todos(nome):
    pasta = BASE_DIR / "data" / "processed"
    resultado = []
    for arquivo in pasta.glob("*.json"):
        with open(arquivo, "r", encoding="utf-8") as f:
            json_info = json.load(f)
        for dados in json_info:
            if nome == dados.get('vacina').lower():
                resultado.append({'nome' : dados['vacina'].lower(), 'idade' : dados['idade_min'], 'grupo' : dados['grupo'].lower()})
    return resultado