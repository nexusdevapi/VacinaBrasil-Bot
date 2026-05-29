from data_handler.scraping_cnes import buscar_ubs_por_municipio

def get_ubs(uf, municipio_id):
    data = buscar_ubs_por_municipio(municipio_id)

    if not data:
        return []

    ubs = []

    for item in data:
        ubs.append({
            "nome": item.get("noFantasia"),
            "endereco": item.get("noLogradouro"),
            "telefone": item.get("nuTelefone")
        })

    return ubs[:3]