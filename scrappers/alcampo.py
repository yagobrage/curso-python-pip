import requests
from bs4 import BeautifulSoup
import csv
import re

def main():
    print('Iniciando scraping...')

    # URL de la página de Alcampo
    url = "https://www.latiendaencasa.es/deportes/search/?v=Deportes&w=2013.40090255016&x=2013.36387191016&s=zapatillas+nike&hierarchy=deportes%2Cactividades-deportivas%2Ctenis-y-padel%2Cpalas-y-raquetas&deep_search=&stype=text_box"  # Cambia esto a la URL específica que deseas scrapear

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Hacer la petición GET
    response = requests.get(url, headers=headers)
    print(f'Respuesta: {response.status_code}')

    # Verificamos que la petición fue exitosa
    if response.status_code == 200:
        # Analizar el HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar los productos, imágenes, precios y nombres
        id_productos = soup.find_all("div", attrs={'data-productid': True})
        url_productos = soup.find_all('link', {'itemprop': 'url'})
        nombres_productos = soup.find_all("p", class_="product_preview-desc")
        precios_productos = soup.find_all("span", class_="price")
        image_tags = soup.find_all('meta', {'itemprop': 'image'})

        # Obtener las URLs de las imágenes
        image_urls = []
        for tag in image_tags:
            img_url = tag.get('content')
            # Si la URL no tiene un dominio completo, añadirlo
            if img_url and not img_url.startswith('http'):
                img_url = 'https:' + img_url
            image_urls.append(img_url)

        # Extraer los datos
        nombres = [n.text.strip() for n in nombres_productos]
        precios = [p.text.strip() for p in precios_productos]
        ids = [j.get('data-productid') for j in id_productos]  # Extract data-productid
        urls = [u.get('href') for u in url_productos]

        # Crear una lista de productos con su nombre, precio, imagen, etc.
        productos = []
        for nombre, precio, imagen, producto_id, producto_url in zip(nombres, precios, image_urls, ids, urls):
            # Limpiar precio y extraer solo los números
            precio_numeros = re.findall(r'\d+\.\d+|\d+', precio)
            if precio_numeros:
                precio_formateado = float(precio_numeros[0])  # Usamos float por si hay decimales
            else:
                precio_formateado = 'N/A'

            productos.append({
                'ID': producto_id,
                'Producto': nombre,
                'Precio': precio_formateado,
                'Imagen': imagen,
                'URL': producto_url
            })

        # Escribir los productos en un archivo CSV
        with open('laTiendaEnCasa.csv', mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['ID','Producto', 'Precio', 'Imagen', 'URL']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()

            for producto in productos:
                csv_writer.writerow(producto)

        print('Datos guardados en productos.csv')
    
    else:
        print("Error al acceder a la página:", response.status_code)

if __name__ == '__main__':
    main()
