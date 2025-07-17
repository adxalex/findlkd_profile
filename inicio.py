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
CHROMEDRIVER_PATH = BASE_DIR / "chromedriver-win64" / "chromedriver.exe"  # ajusta si tu ruta es distinta
CHROME_BINARY_PATH = BASE_DIR / "chrome-win64" / "chrome.exe"  # opcional: solo si usas Chrome portable

# === CONFIGURACIÓN SELENIUM ===
options = Options()
options.add_argument("--headless=new")  # modo sin UI (Chrome moderno)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Si quieres forzar usar el Chrome que descargaste (portable):
if CHROME_BINARY_PATH.exists():
    options.binary_location = str(CHROME_BINARY_PATH)

service = Service(executable_path=str(CHROMEDRIVER_PATH))
driver = webdriver.Chrome(service=service, options=options)

# === PARÁMETROS DE BÚSQUEDA ===
search_query = 'site:linkedin.com/in "tech lead" AND python AND kubernetes AND España'
etiquetas = 'tech lead, python, kubernetes, España'
csv_file = 'resultados_busqueda_google.csv'
num_pages = 3  # número de páginas de resultados de Google

# === EJECUCIÓN ===
results = []
fecha = datetime.today().strftime('%Y-%m-%d')
base_url = "https://www.google.com/search?q=" + search_query.replace(" ", "+")

for page in range(num_pages):
    url = f"{base_url}&start={page * 10}"
    driver.get(url)
    time.sleep(2)  # pequeño delay; puedes mejorar con WebDriverWait

    # Selector de enlaces orgánicos en resultados de Google
    links = driver.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a')
    for link in links:
        href = link.get_attribute('href')
        if href:
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

print(f"✅ Búsqueda completada. {len(results)} resultados guardados en {csv_file}")
