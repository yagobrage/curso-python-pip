import cloudscraper
from bs4 import BeautifulSoup
import json
import re

scraper = cloudscraper.create_scraper()

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0",
    'Accept': "*/*",
    'Accept-Language': "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
    'DNT': "1",
    'Connection': "keep-alive",
    'Cache-Control': "max-age=0",
    'TE': "Trailers"
}

keywords = ['mesa', 'silla', 'escritorio']

for keyword in keywords:
    print(f'\nBuscando productos para keyword: "{keyword}"')
    url_busqueda = f'https://www.bauhaus.es/buscar/productos?text={keyword}&user_search=true&shownProducts=108'
    response = scraper.get(url_busqueda, headers=headers)

    if response.status_code != 200:
        print(f'Error al cargar la página de búsqueda ({response.status_code})')
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    total_tag = soup.find('span', class_='page-title__addition')
    if not total_tag:
        print('No se encontró el div con la cantidad total de productos')
        continue

    numeros = re.findall(r'\d+', total_tag.text)
    if not numeros:
        print('No se pudo extraer el número de productos con regex')
        continue

    total_productos = int(numeros[0])
    print(f'Productos encontrados: {total_productos}')

    if total_productos < 720:
        print('Menos de 720 productos. No se scrapea esta keyword.')
        continue

    productos = []
    single_page = 20  # Comenzamos con la primera página (20 productos)

    # Primera recopilación de productos en la URL de búsqueda original
    while len(productos) < 720:
        if len(productos) == 0:
            url_full = url_busqueda  # Usamos la URL inicial solo en la primera iteración
        else:
            url_full = f'https://www.bauhaus.es/buscar/productos?text={keyword}&user_search=true&shownProducts={len(productos)+108}&singlePage={single_page}'

        response = scraper.get(url_full, headers=headers)

        if response.status_code != 200:
            print(f'Error al cargar la página de productos ({response.status_code})')
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        contenedores = soup.find_all('li', class_='product-list-tiles__item')

        if not contenedores:
            print('No se encontraron productos en la página')
            break

        for contenedor in contenedores:
            tile = contenedor.find('div', class_='product-list-tile')
            if not tile:
                print('Contenedor sin tile. Se omite.')
                continue

            producto_id = tile.get('data-product-code')
            nombre_tag = contenedor.find('div', class_='product-list-tile__info__line')
            precio_tag = contenedor.find('div', class_='price-tag')
            imagen_tag = contenedor.find('img', class_='img-fluid')
            link_tag = contenedor.find('a', class_='product-list-tile__image')

            if not all([producto_id, nombre_tag, precio_tag, imagen_tag, link_tag]):
                print('Producto incompleto. Se omite toda la keyword.')
                break  # Esto termina el scraping de esta keyword y pasa a la siguiente

            try:
                precio = float(precio_tag.get('data-product-price', '0'))
            except ValueError:
                print(f'Error al convertir precio: {precio_tag}')
                precio = 0.0

            productos.append({
                'producto_id': producto_id,
                'nombre': nombre_tag.text.strip(),
                'precio': precio,
                'imagen': imagen_tag.get('src'),
                'url': 'https://www.bauhaus.es' + link_tag.get('href')
            })

        else:
            # Si no hubo un 'break' en los productos (es decir, todos son completos), continuamos con la siguiente página
            single_page += 1
            print(f'Página {single_page} cargada. Productos obtenidos hasta ahora: {len(productos)}')
            continue
        
        # Si llegamos aquí, significa que hubo un break (producto incompleto)
        break  # Salimos del bucle de productos y pasamos a la siguiente keyword

    if productos:
        filename = f'bauhaus-{keyword}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(productos, f, indent=4, ensure_ascii=False)
        print(f'{len(productos)} productos guardados en {filename}')
    else:
        print('No se guardaron productos porque la lista está vacía')
