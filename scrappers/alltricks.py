from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import re
import json

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=opts)
driver.get('https://www.alltricks.es/C-40425-bicicletas')

try:
    wait = WebDriverWait(driver, 10)
    cookies = driver.find_element(By.ID, 'didomi-notice-agree-button')
    cookies.click()

    # Espera a que se vea la opción de cerrar
    close = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'close-btn')))
    close.click()
except:
    pass

def scrollear(driver):
    while True:
        try:
            boton = driver.find_element(By.CLASS_NAME, 'pager-link')
            if boton.is_displayed():
                ActionChains(driver).move_to_element(boton).click().perform()
                break
        except NoSuchElementException:
            pass

        driver.execute_script("window.scrollBy(0, window.innerHeight * 1.5);")
        time.sleep(4)  # Pausa para que se carguen nuevos productos

productos = []
def scrapear():
    print("Scrapeando")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "alltricks-Product-link-wrapper"))
        )
    except:
        print("Error: No se pudieron cargar los productos a tiempo.")
        return
    
    contenedores = driver.find_elements(By.CLASS_NAME, "alltricks-Product-link-wrapper")
    
    for contenedor in contenedores:
        id = contenedor.get_attribute('data-product-id')
        
        nombre = contenedor.find_element(By.CLASS_NAME, 'alltricks-Product-description').text

        try:
            contenedor_precio = contenedor.find_element(By.CLASS_NAME, 'alltricks-Product-actualPrice')
            precio_re = contenedor_precio.find_element(By.TAG_NAME, 'span').text
            precio_s = re.sub(r"[^\d,]", "", precio_re).replace(',', '.')
            precio = float(precio_s)
        except Exception as e:
            print(e)
            precio = None


        try:
            contenedor_precio_antes = contenedor.find_element(By.CLASS_NAME, 'alltricks-Recommended-retail-price')
            precio_antes_re = contenedor_precio_antes.find_element(By.TAG_NAME, 'span').text
            precio_str = re.sub(r"[^\d,]", "", precio_antes_re).replace('.', '').replace(',', '.')
            precio_antes = float(precio_str)
        except:
            precio_antes = None


        contenedor_img = WebDriverWait(contenedor, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alltricks-Product-picture'))
        )
        imagen = contenedor_img.find_element(By.TAG_NAME, 'img').get_attribute('src')


        url = contenedor.find_element(By.CLASS_NAME, 'alltricks-Product-description').get_attribute('href')

        ids = []

        if id not in ids:
            productos.append({
                'id': id,
                'nombre': nombre,
                'precio': precio,
                'precio_antes': precio_antes,
                'imagen': imagen,
                'url': url
            })
            ids.append(id)


for i in range(10):
    print(f"(Scrolleando seccion{i})")
    scrollear(driver)

scrapear()

with open('alltricks.json', mode='w') as file:
    json.dump(productos, file, indent=4, ensure_ascii=False)

print(f'Se han guardado {len(productos)} en el JSON')

