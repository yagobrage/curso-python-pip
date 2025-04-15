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

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

keyword = input("Introduce la keyword: ")#pedir bsuqueda

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=opts)
driver.get('https://www.adidas.es')
sleep(4)

# Aceptar cookies si aparecen
try:
    cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@data-auto-id='glass-gdpr-default-consent-accept-button']"))
    )
    cookies_button.click()
    print("Cookies aceptadas.")
except:
    print("No se encontró el botón de cookies o no fue necesario aceptarlas.")

keyword = "pantalones hombre"

def buscar(keyword):
    buscar = driver.find_element(By.XPATH, "//*[@data-auto-id='mobile-search-icon']")
    buscar.click()
    buscar_input = driver.find_element(By.XPATH, "//*[@data-auto-id='searchinput-mobile']")
    buscar_input.send_keys(keyword)
    sleep(1)
    buscar_input.send_keys(Keys.RETURN)
    sleep(5)



productos_scrapeados = []


def scrapear():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@data-testid='plp-product-card']"))
        )
    except:
        print("Error: No se pudieron cargar los productos a tiempo.")
        return
    
    productos = driver.find_elements(By.XPATH, "//*[@data-testid='plp-product-card']")

    # Esperar hasta que todos los precios originales estén cargados
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "_priceHistory_dg2yj_50"))
        )
        print("Precios originales cargados.")
    except:
        print("Error: No se pudieron cargar todos los precios originales a tiempo.")
    
    for producto in productos:
        try:
            nombre = producto.find_element(By.XPATH, ".//*[@data-testid='product-card-title']").text

            imagen = producto.find_element(By.XPATH, ".//*[@data-testid='product-card-primary-image']").get_attribute('src')

            enlace = producto.find_element(By.XPATH, ".//*[@data-testid='product-card-description-link']").get_attribute('href')

            # Buscar el div con el data-testid='main-price' y extraer el precio visible
            try:
                main_price_div = producto.find_element(By.XPATH, ".//*[@data-testid='main-price']")
                # Precio visible
                precio = float(main_price_div.find_element(By.XPATH, ".//span[not(contains(@class, '_visuallyHidden_dg2yj_2'))]").text.replace(' ','').replace(',','.').replace('\u20ac', ''))
            except:
                precio = None

            precio_original = None  # Asignar valor por defecto a precio_original
            ultimo_precio = None  # Asignar valor por defecto a precio_original
            try:
                price_content_div = producto.find_element(By.CLASS_NAME, "_priceHistory_dg2yj_50")

                # Precio original (dentro de un span)
                try:
                    precio_original_div = price_content_div.find_element(By.CLASS_NAME, "_originalPrice_dg2yj_65")
                    precio_original = float(precio_original_div.find_element(By.TAG_NAME, 'span').text.replace(' ','').replace(',','.').replace('\u20ac', '').replace('Preciooriginal',''))

                except:
                    pass  # Si no se encuentra, dejamos precio_original como None
            
                # Precio original (dentro de un span)
                try:
                    ultimo_precio_div = price_content_div.find_element(By.CLASS_NAME, "_lastLowestPrice_dg2yj_61")
                    ultimo_precio = float(ultimo_precio_div.find_element(By.TAG_NAME, 'span').text.replace(' ','').replace(',','.').replace('\u20ac', '').replace('Últimomejorprecio',''))

                except:
                    pass  # Si no se encuentra, dejamos precio_original como None

            except:
                pass

            # Crear el diccionario de datos del producto
            producto_data = {
                'nombre': nombre,
                'precio': precio,
                'ultimo_precio': ultimo_precio,
                'precio_original': precio_original,
                'imagen': imagen,
                'enlace': enlace
            }

            productos_scrapeados.append(producto_data)

        except Exception as e:
            print(f"Error procesando un producto: {e}")
            print(f"Producto HTML: {producto.get_attribute('outerHTML')}")



def wait_and_click_next():
    try:
        # Esperar hasta que haya al menos dos flechas de paginación visibles
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, ".//*[@data-testid='pagination-next-button']")
            )
        )

        # Seleccionar específicamente la segunda flecha (la que apunta a la derecha →)
        next_btn = driver.find_element(By.XPATH, ".//*[@data-testid='pagination-next-button']")

        # Forzar scroll y clic
        driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
        sleep(0.8)
        driver.execute_script("arguments[0].click();", next_btn)
        sleep(3.5)

        return True

    except Exception as e:
        print(f"Error pasando de página: {e}")
        return False


# Ejecutar búsqueda y scraping
buscar(keyword)


# Recorrer hasta 13 páginas
for pagina in range(13):
    print(f"Scrapeando página {pagina + 1}...")
    
    scrapear()
    
    if not wait_and_click_next():
        break

# Guardamos los resultados en un archivo JSON
with open('adidas.json', 'w', encoding='utf-8') as f:
    json.dump(productos_scrapeados, f, indent=2, ensure_ascii=False)


# Cerrar el navegador
driver.quit()

# Imprimir el número de productos scrapeados
print(f"Scraping completado. {len(productos_scrapeados)} productos guardados en 'adidas.json'.")
