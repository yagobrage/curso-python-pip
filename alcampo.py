import requests
from bs4 import BeautifulSoup

# URL de la página de Alcampo
url = "https://www.latiendaencasa.es/"  # Cambia esto a la URL específica que deseas scrapear

# Hacer la petición GET
response = requests.get(url)

# Verificamos que la petición fue exitosa
if response.status_code == 200:
    # Analizar el HTML
    soup = BeautifulSoup(response.text, "html.parser")

    nombres_productos = soup.find_all("p", class_="h4")

    # Extraer y mostrar los nombres
    for nombre in nombres_productos:
        print(nombre.text.strip())
else:
    print("Error al acceder a la página:", response.status_code)
