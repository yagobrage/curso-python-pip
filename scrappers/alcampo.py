from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re
import json
from selenium.common.exceptions import NoSuchElementException

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=opts)
driver.get('https://www.compraonline.alcampo.es/')


try:
    cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    cookies.click()
except:
    pass

def buscar(keyword):
    input_buscar = driver.find_element(By.ID, 'search')
    input_buscar.click()
    input_buscar.send_keys(keyword)
    elemento = driver.find_element(By.CSS_SELECTOR, 'svg.icon--search')
    elemento.click()


productos = []
def scrapear():
    WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'sc-filq44-0'))
)
    contenedores = driver.find_elements(By.CLASS_NAME, 'sc-filq44-0')

    for contenedor in contenedores:

        id = contenedor.get_attribute('data-test').replace('fop-wrapper:','')
        
        WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'title-container'))
)
        contenedor_titulo = contenedor.find_element(By.CLASS_NAME, 'title-container')
        enlace = contenedor_titulo.find_element(By.TAG_NAME, 'a')

        nombre = enlace.get_attribute('aria-label')

        try:
            precio_raw = contenedor.find_element(By.CSS_SELECTOR, '[data-test="fop-price"]').text
            precio_limpio = re.sub(r"[^\d,]", "", precio_raw).replace(",", ".")
            precio = float(precio_limpio)
        except NoSuchElementException:
            precio = None

        url = enlace.get_attribute('href')

        contenedor_imagen = contenedor.find_element(By.CLASS_NAME, 'image-container')

        
        imagen = contenedor_imagen.find_element(By.TAG_NAME, 'img').get_attribute('src')

        productos.append({
            'id': id,
            'nombre': nombre,
            'precio': precio,
            'imagen': imagen,
            'url': 'https://www.compraonline.alcampo.es' + url
        })

buscar('cola')
scrapear()
print(productos)
