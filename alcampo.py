import requests
from bs4 import BeautifulSoup
import csv
import re

def main():
    print('Hola')
    
        # URL de la página de Alcampo
    url = "https://www.latiendaencasa.es/deportes/search/?v=Deportes&w=2013.40090255016&x=2013.36387191016&s=zapatillas+nike&hierarchy=deportes%2Cactividades-deportivas%2Ctenis-y-padel%2Cpalas-y-raquetas&deep_search=&stype=text_box"  # Cambia esto a la URL específica que deseas scrapear

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    # Hacer la petición GET
    response = requests.get(url, headers=headers)
    print(f'responmse {response.status_code}')
    print('HOLA')
    # Verificamos que la petición fue exitosa
    if response.status_code == 200:
        # Analizar el HTML
        soup = BeautifulSoup(response.text, "html.parser")

        nombres_productos = soup.find_all("p", class_="product_preview-desc")

        precios_productos = soup.find_all("span", class_="price")

        nombres = [n.text.strip() for n in nombres_productos]
        precios = [p.text.strip() for p in precios_productos]


        # Extraer y mostrar los nombres
        productos = {nombre: precio for (nombre,precio) in zip(nombres,precios)}


        with open('productos.csv', mode='w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=('Producto', 'Precio'))
            csv_writer.writeheader()
            for nombre, precio in productos.items():
                            # Limpiar precio y extraer solo los números
                            precio_numeros = re.findall(r'\d+\.\d+|\d+', precio)  # Encuentra números con decimales o sin ellos
                            if precio_numeros:
                                precio_formateado = float(precio_numeros[0])  # Usamos float por si hay decimales
                                csv_writer.writerow({'Producto': nombre, 'Precio': precio_formateado})
                            else:
                                csv_writer.writerow({'Producto': nombre, 'Precio': 'N/A'})  # Si no se encuentra un precio válido


    else:
        print("Error al acceder a la página:", response.status_code)


if __name__ == '__main__':
    main()