from pathlib import Path
from datetime import datetime, timedelta

from data_handler.scraping import gerar_calendario_vacinas

BASE_DIR = Path(__file__).resolve().parents[1]
ARQUIVO_JSON = BASE_DIR / "data" / "processed" / "calendario_vacinas.json"


def precisa_update():
    if not ARQUIVO_JSON.exists():
        return True

    data_modificacao = datetime.fromtimestamp(ARQUIVO_JSON.stat().st_mtime)
    return datetime.now() - data_modificacao > timedelta(days=7)


def se_precisar_update():
    try:
        if precisa_update():
            gerar_calendario_vacinas()
            return True
        return False
    except Exception as e:
        print(f"Erro no update: {e}")
        return False