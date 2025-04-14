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

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=opts)
driver.get('https://www.aboutyou.es/')

#palabra para la busqueda
keyword = "Zapatos de hombre"


def buscar(keyword):
    search_icon = driver.find_element(By.CSS_SELECTOR, '[data-testid="searchIcon"]')
    search_icon.click()
    search_field = driver.find_element(By.CSS_SELECTOR, '[data-testid="searchBarInput"]')  #input
    search_field.send_keys(keyword) #escirbir en input
    sleep(1)
    search_field.send_keys(Keys.RETURN) #hacer enter


ids, nombres, precios, precios_antes, enlaces, imagenes = [], [], [], [], [], []

def scrapear():
    contenedores = driver.find_elements(By.CLASS_NAME, 'she0wnd')
    for contenedor in contenedores:
        try:
            id_sin_formato = contenedor.get_attribute('data-testid')
            id = ''.join(re.findall(r'\d+', id_sin_formato))  # Solo números como string

            nombre = contenedor.find_element(By.CSS_SELECTOR, '[data-testid="productName"]').text

            precio = float(contenedor.find_element(By.CSS_SELECTOR, '[data-testid="finalPrice"]').text
                           .replace('\u20ac', '').replace('.', '').replace(',', '.').replace(' ', '').replace('desde',''))
            
            enlace = contenedor.find_element(By.TAG_NAME, 'a').get_attribute('href')

            imagen_elem = contenedor.find_element(By.CSS_SELECTOR, '[data-testid="productImage"]')
            imagen = imagen_elem.find_element(By.TAG_NAME, 'img').get_attribute('src')

            try:
                precio_antes = float(contenedor.find_element(By.CSS_SELECTOR, '[data-testid="StruckPrice"]').text
                                     .replace('\u20ac', '').replace('.', '').replace(',', '.').replace(' ', '').replace('desde',''))
            except:
                precio_antes = None

            if id not in ids:  # Evitar duplicados
                ids.append(id)
                nombres.append(nombre)
                precios.append(precio)
                precios_antes.append(precio_antes)
                enlaces.append(enlace)
                imagenes.append(imagen)

        except Exception as e:
            print(f"Error al scrapear un producto: {e}")
            continue


buscar(keyword)
# Espera a que los resultados de la búsqueda estén visibles
sleep(4)

# Número de páginas que queremos cargar (definidas por el alto del viewport)
paginas_a_cargar = 30

# Cuántas pantallas queremos saltar por scroll
pantallas_por_scroll = 3

# Obtenemos la altura del viewport
viewport_height = driver.execute_script("return window.innerHeight")

for i in range(1, (paginas_a_cargar // pantallas_por_scroll) + 1):
    print(f'Scrapeando sección {i}...')
    
    # Calculamos la posición a la que queremos hacer scroll
    scroll_position = viewport_height * pantallas_por_scroll * i
    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
    
    # Esperamos un poco para que se cargue el contenido dinámico
    sleep(2)
    
    # Ejecutamos el scraping
    scrapear()

# Mostrar resultados en json
productos = []

for id, nombre, precio, precio_antes, enlace, imagen in zip(ids, nombres, precios, precios_antes, enlaces, imagenes):
    productos.append({
        "id": id,
        "nombre": nombre,
        "precio": precio,
        "precio_antes": precio_antes,
        "enlace": enlace,
        "imagen": imagen
    })
with open("aboutyou.json", "w") as f:
    json.dump(productos, f, indent=4, ensure_ascii=False)

print(f"Se han añadido {len(productos)} al JSON")

driver.quit()
