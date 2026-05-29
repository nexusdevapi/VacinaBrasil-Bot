from data_handler.cnes_para_id import resolver_municipio_id
from data_handler.scraping_ubs import get_ubs

def processar_ubs(uf, cidade):
    municipio_id = resolver_municipio_id(uf, cidade)

    if not municipio_id:
        return "Não consegui encontrar essa cidade."

    ubs = get_ubs(uf, municipio_id)

    if not ubs:
        return "Nenhuma UBS encontrada."

    texto = "🏥 UBS próximas:\n\n"

    for u in ubs:
        texto += f"📍 {u['nome']}\n"
        texto += f"🏠 {u['endereco']}\n"
        texto += f"📞 {u['telefone']}\n\n"

    return texto