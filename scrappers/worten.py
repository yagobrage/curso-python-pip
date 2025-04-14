import json
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

# Configuración del navegador con user-agent
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=opts)
driver.get('https://www.worten.es')
sleep(2)  # Reducimos un poco el tiempo de espera inicial

# Aceptar cookies si aparece el botón
try:
    cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'button--primary') and contains(., 'Aceptar')]"))
    )
    cookies_button.click()
    print("Cookies aceptadas.")
except:
    print("No se encontró el botón de cookies o no fue necesario aceptarlas.")

keyword = "iphone"  # Cambiar para buscar

def buscar(keyword):
    buscar = driver.find_element(By.CSS_SELECTOR, 'input#search')
    buscar.click()
    buscar.send_keys(keyword)  # Escribir en input
    sleep(1)
    buscar.send_keys(Keys.RETURN)  # Hacer enter

# Lista global de productos
productos_scrapeados = []

def scrapear():
    # Esperar hasta que los productos se carguen en la página
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'listing-content__card'))
        )
    except:
        print("Error: No se pudieron cargar los productos a tiempo.")
        return
    
    productos = driver.find_elements(By.CLASS_NAME, 'listing-content__card')

    for producto in productos:
        try:
            # Verificar si el producto tiene el atributo 'hidden'
            if producto.get_attribute('hidden') is not None:
                continue

            # Buscar enlace y data-sku
            a_tag = producto.find_element(By.XPATH, ".//a[contains(@class, 'product-card')]")
            enlace = a_tag.get_attribute('href')
            id = a_tag.get_attribute('data-sku')
            producto_id = ''.join(re.findall(r'\d+', id)) 

            # Verificar que el producto_id no esté ya en la lista
            if any(p['id'] == producto_id for p in productos_scrapeados):
                continue  # Si el id ya está en la lista, saltar este producto

            # Imagen y nombre
            imagen = producto.find_element(By.TAG_NAME, 'img').get_attribute('src')
            nombre = producto.find_element(By.CLASS_NAME, 'product-card__name').text.strip()

            # Precio
            spans = producto.find_element(By.CLASS_NAME, 'value')
            decimals = producto.find_element(By.CLASS_NAME, 'decimal')

            entero = spans.text.strip().replace('.', '')
            decimal = decimals.text.strip()
            precio = float(f"{entero}.{decimal}")

            # Crear el diccionario de datos del producto
            producto_data = {
                'id': producto_id,
                'nombre': nombre,
                'precio': precio,
                'enlace': 'https://www.worten.es' + enlace if enlace.startswith('/') else enlace,
                'imagen': imagen
            }

            # Añadir el producto a la lista de productos scrapeados
            productos_scrapeados.append(producto_data)

        except Exception as e:
            print(f"Error procesando un producto: {e}")
            print(f"Producto HTML: {producto.get_attribute('outerHTML')}")

def wait_and_click_next():
    try:
        # Esperar hasta que haya al menos dos flechas de paginación visibles
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(@class, 'numbers-pagination__icons--light')]")
            )
        )

        # Seleccionar específicamente la segunda flecha (la que apunta a la derecha →)
        next_btn = driver.find_element(By.XPATH, "(//div[contains(@class, 'numbers-pagination__icons--light')])[2]")

        # Forzar scroll y clic
        driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
        sleep(0.8)
        driver.execute_script("arguments[0].click();", next_btn)
        sleep(3.5)

        return True

    except Exception as e:
        print(f"Error pasando de página: {e}")
        return False

# Llamar a la función para buscar el producto
buscar(keyword)

# Esperar un poco para asegurarnos de que la página esté cargada
sleep(3)

# Recorrer hasta 10 páginas
for pagina in range(10):
    print(f"Scrapeando página {pagina + 1}...")
    
    scrapear()
    
    if not wait_and_click_next():
        break

# Guardamos los resultados en un archivo JSON
with open('worten.json', 'w', encoding='utf-8') as f:
    json.dump(productos_scrapeados, f, indent=2, ensure_ascii=False)

# Cerrar el navegador
driver.quit()

# Imprimir el número de productos scrapeados
print(f"Scraping completado. {len(productos_scrapeados)} productos guardados en 'worten.json'.")
