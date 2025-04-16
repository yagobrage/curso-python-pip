from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=opts)
driver.get('https://www.zara.com/es/es/search/home')

try:
    sleep(3)
    cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    cookies.click()

except:
    pass

def scroll(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(5)

keyword = 'Pantalones'
def buscar(keyword):

    categoria = driver.find_element(By.XPATH, "//button[contains(@class, 'search-sections-bar__section-button') and normalize-space(text())='Hombre']")
    categoria.click()

    input = driver.find_element(By.ID, 'search-home-form-combo-input')
    input.click()

    input.send_keys(keyword)
    sleep(1)
    input.send_keys(Keys.RETURN)
    sleep(4)

productos = []
def scrapear():
    print('Scrapeando...')
    WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-grid-product--is-not-template"))
        )

    contenedores = driver.find_elements(By.CLASS_NAME, 'product-grid-product--is-not-template')

    for contenedor in contenedores:

        id = contenedor.get_attribute('data-productid')
        
        titulo = contenedor.find_element(By.CLASS_NAME, 'product-grid-product-info__name')

        nombre = titulo.find_element(By.TAG_NAME, 'h2').text

        url = titulo.get_attribute('href')

        precio_elem = contenedor.find_element(By.CLASS_NAME, 'price-current__amount')

        precio = precio_elem.find_element(By.CLASS_NAME, 'money-amount__main').text

        imagen_elem = contenedor.find_element(By.CLASS_NAME, 'media__wrapper--fill')
        imagen = imagen_elem.find_element(By.TAG_NAME, 'img').get_attribute('src')

        ids = []

        if id not in ids:
            productos.append({
                'id': id,
                'nombre': nombre,
                'precio':precio,
                'url': url,
                'imagen': imagen
            })

            ids.append(id)



buscar(keyword=keyword)

for i in range(10):
    print(f'Scrollenado seccion {i}...')
    scroll(driver)
scrapear()

# Guardar productos en un archivo JSON
with open('zara.json', mode='w') as file:
    json.dump(productos, file, indent=4, ensure_ascii=False)

print(f"{len(productos)} Productos escritos en JSON") 
