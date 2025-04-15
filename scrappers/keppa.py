from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=opts)
driver.get('https://keepa.com/#!deals/%7B%22page%22%3A0%2C%22domainId%22%3A%229%22%2C%22excludeCategories%22%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C%22includeCategories%22%3A%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%5D%2C%22priceTypes%22%3A%5B0%5D%2C%22deltaRange%22%3A%5B0%2C10000%5D%2C%22deltaPercentRange%22%3A%5B20%2C80%5D%2C%22salesRankRange%22%3A%5B-1%2C-1%5D%2C%22currentRange%22%3A%5B500%2C40000%5D%2C%22minRating%22%3A-1%2C%22isLowest%22%3Afalse%2C%22isLowest90%22%3Afalse%2C%22isLowestOffer%22%3Afalse%2C%22isOutOfStock%22%3Afalse%2C%22titleSearch%22%3A%22%22%2C%22isRangeEnabled%22%3Atrue%2C%22isFilterEnabled%22%3Afalse%2C%22filterErotic%22%3Atrue%2C%22singleVariation%22%3Atrue%2C%22hasReviews%22%3Afalse%2C%22isPrimeExclusive%22%3Afalse%2C%22mustHaveAmazonOffer%22%3Afalse%2C%22mustNotHaveAmazonOffer%22%3Afalse%2C%22sortType%22%3A1%2C%22dateRange%22%3A1%2C%22warehouseConditions%22%3A%5B1%2C2%2C3%2C4%2C5%5D%2C%22settings%22%3A%7B%22viewTyp%22%3A0%7D%2C%22perPage%22%3A150%2C%22websiteDisplayGroupName%22%3A%5B%5D%2C%22websiteDisplayGroup%22%3A%5B%5D%2C%22type%22%3A%5B%5D%2C%22manufacturer%22%3A%5B%5D%2C%22brand%22%3A%5B%5D%2C%22brandStoreName%22%3A%5B%5D%2C%22brandStoreUrlName%22%3A%5B%5D%2C%22productGroup%22%3A%5B%5D%2C%22model%22%3A%5B%5D%2C%22color%22%3A%5B%5D%2C%22size%22%3A%5B%5D%2C%22unitType%22%3A%5B%5D%2C%22scent%22%3A%5B%5D%2C%22itemForm%22%3A%5B%5D%2C%22pattern%22%3A%5B%5D%2C%22style%22%3A%5B%5D%2C%22material%22%3A%5B%5D%2C%22itemTypeKeyword%22%3A%5B%5D%2C%22targetAudienceKeyword%22%3A%5B%5D%2C%22edition%22%3A%5B%5D%2C%22format%22%3A%5B%5D%2C%22author%22%3A%5B%5D%2C%22binding%22%3A%5B%5D%2C%22languages%22%3A%5B%5D%2C%22partNumber%22%3A%5B%5D%7D')

try:
    wait = WebDriverWait(driver, 10)

    # Clic en el menú para desplegar las opciones
    menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.languageMenuImg')))
    menu.click()

    # Espera a que se vea la opción '.es' en el menú desplegable
    es_option = wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@rel="domain" and @setting="9"]')))
    es_option.click()

    print("Dominio cambiado a .es")

except Exception as e:
    print("Error cambiando el dominio:", e)

# Esperar que los productos estén visibles tras el cambio de dominio
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'productContainer')))

productos = []

def scroll(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(5)  # Espera para cargar los productos tras hacer scroll

def scrapear():
    print('Scrapeando...')
    contenedores_producto = driver.find_elements(By.CLASS_NAME, 'productContainer')

    for contenedor in contenedores_producto:
        id = contenedor.get_attribute('id').replace('p', '')
        nombre = contenedor.find_element(By.CLASS_NAME, 'title').text
        precio = float(contenedor.find_element(By.CLASS_NAME, 'productPriceTableTdLargeS').text.replace('Now: € ',''))
        media = float(contenedor.find_element(By.CLASS_NAME, 'productPriceTableTdSmallS').text.replace('Average: € ',''))
        url = contenedor.find_element(By.TAG_NAME, 'a').get_attribute('href')
        imagen = contenedor.find_element(By.CLASS_NAME, 'productImage').find_element(By.TAG_NAME, 'img').get_attribute('src')

        if id not in [p['id'] for p in productos]:
            productos.append({
                'id': id,
                'nombre': nombre,
                'precio': precio,
                'media': media,
                'url': url,
                'imagen': imagen
            })

    print(f'Se han obtenido {len(productos)}')

# Realiza el scraping y el scroll varias veces
for i in range(11):
    print(f'Scrolleando seccion{i}...')
    scroll(driver)

scrapear()

# Guardar productos en un archivo JSON
with open('keppa.json', mode='w') as file:
    json.dump(productos, file, indent=4, ensure_ascii=False)

print("Productos escritos en JSON")
