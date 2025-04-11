import requests
from bs4 import BeautifulSoup

url = 'https://dockerlabs.es/'

respuesta = requests.get(url)

if respuesta.status_code == 200:
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    maquinas = soup.find_all('div', onclick=True)
    conteo_maquinas = 1

    autores = set()

    for maquina in maquinas:
        onclick_text = maquina['onclick']
        autor = onclick_text.split("'")[7]
        autores.add(autor)

        nombre_maquina = onclick_text.split("'")[1]
        dificultad = onclick_text.split("'")[3]
        conteo_maquinas += 1

        print(f"{nombre_maquina} -> {dificultad} -> {autor}")
    
    print(f"El numero de maquinas es {conteo_maquinas}")
else:
    print(f'Hubo un error en la petición {respuesta.status_code}')