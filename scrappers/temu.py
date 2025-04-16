
url_antigua = '/es/1pieza-separador-de-cascaras-de--de-acero-inoxidable---herramienta-de--de-limpiar-divisor-de--para-navidad-halloween--de--g-601099945349949.html'
pos_id = url_antigua.find('-g-')

if pos_id:

    id = url_antigua[pos_id+1:] #coger todo en adelante

url_base = 'https://www.temu.com/es/'
nueva_url = url_base + id
print(nueva_url)