from playwright.sync_api import sync_playwright

URL = "https://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp"

UF_MAP = {
    "AC": "12","AL": "27","AP": "16","AM": "13","BA": "29","CE": "23",
    "DF": "53","ES": "32","GO": "52","MA": "21","MT": "51","MS": "50",
    "MG": "31","PA": "15","PB": "25","PR": "41","PE": "26","PI": "22",
    "RJ": "33","RN": "24","RS": "43","RO": "11","RR": "14","SC": "42",
    "SP": "35","SE": "28","TO": "17"
}

def resolver_municipio_id(uf, cidade):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL)

        # seleciona UF corretamente (valor numérico)
        page.select_option("select[ng-model='Estado']", UF_MAP[uf])

        # 🔥 espera o select de município ser preenchido (não só existir)
        page.wait_for_function("""
            () => {
                const select = document.querySelector("select[ng-model='Municipio']");
                return select && select.options.length > 1;
            }
        """)

        # agora sim pega as opções
        options = page.query_selector_all("select[ng-model='Municipio'] option")

        cidade = cidade.strip().upper()
        municipio_id = None

        for opt in options:
            text = opt.inner_text().strip().upper()
            value = opt.get_attribute("value")

            if text == cidade:
                municipio_id = value
                break

        browser.close()
        return municipio_id