import re, csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=opts)
driver.get('https://www.worten.es/search?query=iphone')
sleep(4)

productos = driver.find_elements(By.CLASS_NAME, 'listing-content__card')
spans = driver.find_elements(By.CLASS_NAME, 'value')
decimals = driver.find_elements(By.CLASS_NAME, 'decimal')
nombres = driver.find_elements(By.CLASS_NAME, 'product-card__name')

with open('worten.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['nombre', 'precio', 'imagen', 'url'])

    for prod, span, dec, nom in zip(productos, spans, decimals, nombres):
        try:
            enlace = prod.find_element(By.TAG_NAME, 'a').get_attribute('href')
            imagen = prod.find_element(By.TAG_NAME, 'img').get_attribute('src')
            precio = float(re.sub(r'\.', '', span.text) + '.' + dec.text)
            writer.writerow([nom.text, precio, imagen, enlace])
        except Exception as e:
            print(f"Error procesando producto: {e}")

driver.quit()
