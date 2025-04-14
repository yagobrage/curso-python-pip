from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=opts)
driver.get('https://www.chollometro.com/')
sleep(4)

# Aceptar cookies
try:
    cookies = driver.find_element(By.XPATH, "//*[@data-t='acceptAll']")
    cookies.click()
except:
    pass

urls, nombres, precios, precios_antes, imagenes = [], [], [], [], []

#Funcion scrapear
def scrape_page():
    productos = driver.find_elements(By.CLASS_NAME, 'thread-clickRoot')
    for producto in productos:
        try:
            precio_sin_formatear = producto.find_element(By.CLASS_NAME, 'thread-price').text
            precio_sin_formatear = precio_sin_formatear.replace('\u20ac', '').replace('.', '').replace(',', '.')

            precio = float(precio_sin_formatear)

            try:
                precio_antes_sin_formatear = producto.find_element(By.CLASS_NAME, 'text--lineThrough').text
                precio_antes_sin_formatear = precio_antes_sin_formatear.replace('\u20ac', '').replace('.', '').replace(',', '.')

                precio_antes = float(precio_antes_sin_formatear)
            except:
                precio_antes = None  # o "" si prefieres string vacío

            imagen_elem = producto.find_element(By.CLASS_NAME, 'threadListCard-image')
            imagen = imagen_elem.find_element(By.TAG_NAME, 'img').get_attribute('src')

            titulo_elem = producto.find_element(By.CLASS_NAME, 'thread-title')
            enlace = titulo_elem.find_element(By.TAG_NAME, 'a').get_attribute('href')
            nombre = titulo_elem.find_element(By.TAG_NAME, 'a').text

            urls.append(enlace)
            nombres.append(nombre)
            precios.append(precio)
            precios_antes.append(precio_antes)
            imagenes.append(imagen)

        except:
            continue


def wait_and_click_next():
    try:
        #cerrar pop up si lo hay
        cerrar_popup()

        #esperar hasta que cargen los botones de siuiente y pasar de pagina
        wait = WebDriverWait(driver, 10)
        next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Siguiente página"]')))
        driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
        sleep(1)
        next_btn.click()
        sleep(4)
        return True
    except Exception as e:
        print(f"Error pasando de página: {e}")
        return False
    
from selenium.webdriver.common.action_chains import ActionChains

def cerrar_popup():
    try:
        driver.find_element(By.CLASS_NAME, 'popover-cover')
        
        # Click en una zona segura fuera del popup
        ActionChains(driver).move_by_offset(10, 10).click().perform()
        print("Popup cerrado con click.")
        sleep(1)
    except:
        print("No se detectó popup.")



# Recorrer hasta 10 páginas
for pagina in range(10):
    print(f"Scrapeando página {pagina + 1}...")
    
    scrape_page()
    
    if not wait_and_click_next():
        break
driver.quit()


# Mostrar resultados en json
productos = []

for titulo, precio, precio_antes, url, imagen in zip(nombres, precios, precios_antes, urls, imagenes):
    productos.append({
        "titulo": titulo,
        "precio": precio,
        "precio_antes": precio_antes,
        "url": url,
        "imagen": imagen
    })
with open("chollometro.json", "w") as f:
    json.dump(productos, f, indent=4, ensure_ascii=False)

print('Productos escritos en JSON')