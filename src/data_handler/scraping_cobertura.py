from playwright.sync_api import sync_playwright
from pathlib import Path
import pandas as pd
import json
import os
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

URL_COBERTURA = "https://infoms.saude.gov.br/extensions/SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA/SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA.html#"

URL_COVID = "https://infoms.saude.gov.br/extensions/SEIDIGI_DEMAS_COBERTURA_COVID_RESIDENCIA/SEIDIGI_DEMAS_COBERTURA_COVID_RESIDENCIA.html#"

JSON_PATH = OUT_DIR / "cobertura_vacinal.json"


def precisa_update():
    if not JSON_PATH.exists():
        return True
    data_modificacao = datetime.fromtimestamp(JSON_PATH.stat().st_mtime)
    return datetime.now() - data_modificacao > timedelta(days=7)


def esperar(page, t=8000):
    page.wait_for_timeout(t)


def clicar(page, sel):
    el = page.locator(sel)
    el.scroll_into_view_if_needed()
    el.click()


def baixar(page, click_fn, output_path):

    with page.expect_download(timeout=8000) as d:
        click_fn()
        page.wait_for_timeout(4000)

    download = d.value

    final_path = output_path.with_suffix(".xlsx")
    download.save_as(str(final_path))

    return final_path


def baixar_cobertura(page):

    page.goto(URL_COBERTURA, wait_until="domcontentloaded")
    esperar(page, 8000)

    page.locator("#aba2-tab").click(force=True)
    esperar(page, 8000)

    return baixar(
        page,
        lambda: clicar(page, "#exportar-dados-QV1-10"),
        OUT_DIR / "cobertura_vacinal_geral.xlsx"
    )


def baixar_covid_mono(page):

    page.goto(URL_COVID, wait_until="domcontentloaded")
    esperar(page, 8000)

    page.locator("#mono-tab").click(force=True)
    esperar(page, 8000)

    return baixar(
        page,
        lambda: clicar(page, "#exportar-dados-QV1-05"),
        OUT_DIR / "covid_monovalente_municipio.xlsx"
    )


def baixar_covid_mono_uf(page):

    page.goto(URL_COVID, wait_until="domcontentloaded")
    esperar(page, 8000)

    page.locator("#mono-tab").click(force=True)
    esperar(page, 8000)

    return baixar(
        page,
        lambda: clicar(page, "#exportar-dados-QV1-04"),
        OUT_DIR / "covid_monovalente_uf.xlsx"
    )


def baixar_covid_biva(page):

    page.locator("#home-tab").click(force=True)
    esperar(page, 8000)

    return baixar(
        page,
        lambda: clicar(page, "#exportar-dados-QV1-10"),
        OUT_DIR / "covid_bivalente_municipio.xlsx"
    )


def baixar_covid_biva_uf(page):

    page.locator("#home-tab").click(force=True)
    esperar(page, 8000)

    return baixar(
        page,
        lambda: clicar(page, "#exportar-dados-QV1-09"),
        OUT_DIR / "covid_bivalente_uf.xlsx"
    )


def clean(v):
    if pd.isna(v):
        return None
    v = str(v).strip()
    return None if v.lower() == "nan" else v


def parse_xlsx(path, name):

    df = pd.read_excel(path)
    df = df.ffill()

    cols = df.columns.tolist()

    fixed = cols[:5]
    vacina_cols = cols[5:]

    data = {}

    for _, row in df.iterrows():

        occ = clean(row[fixed[0]])
        uf = clean(row[fixed[1]])
        macro = clean(row[fixed[2]])
        reg = clean(row[fixed[3]])
        mun = clean(row[fixed[4]])

        if not all([occ, uf, macro, reg, mun]):
            continue

        data.setdefault(name, {})
        data[name].setdefault(occ, {})
        data[name][occ].setdefault(uf, {})
        data[name][occ][uf].setdefault(macro, {})
        data[name][occ][uf][macro].setdefault(reg, {})
        data[name][occ][uf][macro][reg].setdefault(mun, {})

        target = data[name][occ][uf][macro][reg][mun]

        for col in vacina_cols:
            val = row[col]

            if pd.notna(val):
                try:
                    target[col] = float(val)
                except:
                    target[col] = str(val)

    return data


def run():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        cob = baixar_cobertura(page)

        mono = baixar_covid_mono(page)
        mono_uf = baixar_covid_mono_uf(page)

        biva = baixar_covid_biva(page)
        biva_uf = baixar_covid_biva_uf(page)

        browser.close()

    data = {}
    data.update(parse_xlsx(cob, "cobertura_vacinal_geral"))
    data.update(parse_xlsx(mono, "covid_monovalente_municipio"))
    data.update(parse_xlsx(mono_uf, "covid_monovalente_uf"))
    data.update(parse_xlsx(biva, "covid_bivalente_municipio"))
    data.update(parse_xlsx(biva_uf, "covid_bivalente_uf"))

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    for p in [cob, mono, mono_uf, biva, biva_uf]:
        if os.path.exists(p):
            os.remove(p)

    return JSON_PATH


if __name__ == "__main__":
    if precisa_update():
        run()