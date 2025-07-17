from pathlib import Path
from datetime import datetime
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# === RUTAS ===
BASE_DIR = Path(__file__).resolve().parent
CHROMEDRIVER_PATH = BASE_DIR / "chromedriver-win64" / "chromedriver.exe"
CHROME_BINARY_PATH = BASE_DIR / "chrome-win64" / "chrome.exe"

# === CONFIGURACIÓN SELENIUM ===
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

if CHROME_BINARY_PATH.exists():
    options.binary_location = str(CHROME_BINARY_PATH)

service = Service(executable_path=str(CHROMEDRIVER_PATH))
driver = webdriver.Chrome(service=service, options=options)

# === PARÁMETROS DE BÚSQUEDA ===
search_query = 'site:linkedin.com/in "tech lead" AND (python OR react) AND Madrid'
etiquetas = 'tech lead, python, kubernetes, España'
csv_file = 'resultados_bing_filtrados.csv'
num_pages = 10

# === EJECUCIÓN ===
results = []
fecha = datetime.today().strftime('%Y-%m-%d')
base_url = "https://www.bing.com/search?q=" + search_query.replace(" ", "+")

for page in range(num_pages):
    start = page * 10
    url = f"{base_url}&first={start + 1}"
    driver.get(url)
    time.sleep(2)

    # Selector de resultados en Bing
    links = driver.find_elements(By.XPATH, '//li[@class="b_algo"]//h2/a')
    for link in links:
        href = link.get_attribute('href')
        if (
            href and
            "linkedin.com/in/" in href and
            not any(sub in href for sub in ["jobs", "company", "school", "learning"])
        ):
            results.append({
                'url': href,
                'etiquetas': etiquetas,
                'fecha': fecha
            })

driver.quit()

# === GUARDAR CSV ===
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['url', 'etiquetas', 'fecha'])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Búsqueda completada. {len(results)} perfiles reales guardados en {csv_file}")
