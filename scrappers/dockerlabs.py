import requests
from bs4 import BeautifulSoup
import csv

url = 'https://dockerlabs.es/'

respuesta = requests.get(url)

if respuesta.status_code == 200:
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    maquinas = soup.find_all('div', onclick=True)
    conteo_maquinas = 1
    lista_maquinas = []

    for maquina in maquinas:
        onclick_text = maquina['onclick']
        autor = onclick_text.split("'")[7]

        nombre_maquina = onclick_text.split("'")[1]
        dificultad = onclick_text.split("'")[3]
        conteo_maquinas += 1

        lista_maquinas.append({
            "Nombre": nombre_maquina,
            "Dificultad": dificultad,
            "Autor": autor
        })

    
    # Escribir los productos en un archivo CSV
    with open('scrappers/dockerlabs.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Nombre','Dificultad', 'Autor']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for maquina in lista_maquinas:
            csv_writer.writerow(maquina)

        print('Datos guardados en dockerlabs.csv')
    
    print(f"El numero de maquinas es {conteo_maquinas}")
else:
    print(f'Hubo un error en la petición {respuesta.status_code}')