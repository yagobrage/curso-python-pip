from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
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

def scrollear(driver):
        driver.execute_script("window.scrollBy(0, window.innerHeight * 1.5);")
        sleep(5)  # Pausa para que se carguen nuevos productos


productos = []
def scrapear():
    # Esperar a que los contenedores de productos estén presentes
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-test^="fop-wrapper"]'))
    )
    contenedores = driver.find_elements(By.CSS_SELECTOR, '[data-test^="fop-wrapper"]')

    for contenedor in contenedores:
        try:
            # Extraer el ID del producto
            id = contenedor.get_attribute('data-test').replace('fop-wrapper:', '')

            # Extraer el nombre del producto utilizando el atributo aria-label
            enlace = contenedor.find_element(By.CSS_SELECTOR, 'a[aria-label]')
            nombre = enlace.get_attribute('aria-label')

            # Extraer el precio del producto
            try:
                precio_raw = contenedor.find_element(By.CSS_SELECTOR, '[data-test="fop-price"]').text
                precio_limpio = re.sub(r"[^\d,]", "", precio_raw).replace(",", ".")
                precio = float(precio_limpio)
            except NoSuchElementException:
                precio = None

            # Extraer la URL del producto
            url = enlace.get_attribute('href')

            # Extraer la URL de la imagen del producto
            try:
                imagen = contenedor.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
            except NoSuchElementException:
                imagen = None

            # Agregar el producto a la lista
            productos.append({
                'id': id,
                'nombre': nombre,
                'precio': precio,
                'imagen': imagen,
                'url': 'https://www.compraonline.alcampo.es' + url
            })

        except Exception as e:
            print(f"Error al procesar el contenedor: {e}")
            continue
buscar('cola')

for i in range(9):
    print(f'Scrolleando seccion {i}') 
    scrollear(driver)
    scrapear()
scrapear()
print(len(productos))
