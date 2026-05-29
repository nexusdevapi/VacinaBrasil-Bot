import requests

def buscar_ubs_por_municipio(municipio_id: str):
    url = f"https://cnes.datasus.gov.br/services/estabelecimentos?municipio={municipio_id}"

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return []
        return r.json()
    except:
        return []