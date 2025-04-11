import requests
from bs4 import BeautifulSoup
import csv
import re
from urllib.parse import urljoin  # Para construir URLs absolutas

url = 'https://books.toscrape.com/'

respuesta = requests.get(url)

if respuesta.status_code == 200:
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    
    lista_nombres = []
    lista_precios = []
    lista_imagenes = []
    lista_urls = []

    libros = []

    # Sacar el container de los productos
    contenedor_productos = soup.find_all('article', class_='product_pod')

    for contenedor in contenedor_productos:
        # Sacar nombres
        nombre = contenedor.find('h3').find('a').get('title')
        lista_nombres.append(nombre)

        # Sacar imagenes y URLs de las imágenes
        imagen = contenedor.find('img').get('src')
        imagen_completa = urljoin(url, imagen)
        lista_imagenes.append(imagen_completa)

        # Sacar enlaces relativos y convertir a absolutos
        enlace_relativo = contenedor.find('a').get('href')
        enlace_completo = urljoin(url, enlace_relativo)  # Construir URL absoluta
        lista_urls.append(enlace_completo)

    # Precios filtro
    precios = soup.find_all('p', class_='price_color')
    for precio in precios:
        lista_precios.append(re.findall(r'\d+\.\d+', precio.text))

    # Guardar libros
    for nombre, precio, imagen, url in zip(lista_nombres,lista_precios,lista_imagenes,lista_urls):
        libro = {
            "Nombre":nombre,
            "Precio":precio,
            "Imagen":imagen,
            "Enlace":url,
        }

        libros.append(libro)

    # Crear Tabla
    with open('scrappers/booksToScrape.csv', mode='w') as file:

        fieldNames = ['Nombre','Precio','Imagen','Enlace']
        writer = csv.DictWriter(file, fieldnames=fieldNames)
        writer.writeheader()

        print("Escribiendo datos")
        for libro in libros:
            writer.writerow(libro)
else: 
    print(f"La petición falló {respuesta.status_code}")
