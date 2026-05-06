import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://infoms.saude.gov.br/extensions/SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA/SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA.html"

dir_download = Path(__file__).resolve().parents[1] / "data" / "processed"
dir_download.mkdir(parents=True, exist_ok=True)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")

prefs = {
    "download.default_directory": str(dir_download),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

try:
    driver.get(URL)

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)

    aba = wait.until(EC.element_to_be_clickable((By.ID, "aba2-tab")))
    driver.execute_script("arguments[0].click();", aba)
    time.sleep(3)

    macro = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(., 'Macrorregiões')]"))
    )
    driver.execute_script("arguments[0].click();", macro)
    time.sleep(3)

    botao_exportar = wait.until(
        EC.element_to_be_clickable((By.ID, "exportar-dados-QV1-10"))
    )
    driver.execute_script("arguments[0].click();", botao_exportar)

    time.sleep(15)

    arquivos = list(dir_download.glob("*.xlsx"))

    if arquivos:
        arquivos.sort(key=lambda x: x.stat().st_mtime)

        arquivo_baixado = arquivos[-1]
        destino = dir_download / "cobertura_vacinal.xlsx"

        if arquivo_baixado != destino:
            if destino.exists():
                destino.unlink()
            arquivo_baixado.rename(destino)

finally:
    driver.quit()