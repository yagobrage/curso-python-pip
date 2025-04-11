class Tarea:
    def __init__(self, id, titulo, descripcion, estado):
        self.id = id,
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado

class ControlTareas:
    def __init__(self):
        self.tareas = []

    def añadirTarea(self, tarea):
            # Comprobamos si ya existe una tarea con el mismo ID
            for i in self.tareas:
                if i['id'] == tarea['id']:
                    print(f"Ya existe una tarea con el ID {tarea['id']}")
                    return
            
            # Si no existe una tarea con ese ID, la agregamos
            self.tareas.append(tarea)
            print(f"Tarea con ID {tarea['id']} añadida exitosamente.")
            
            # Actualizamos el archivo después de añadir una tarea
            self.actualizarArchivoTareas()

    def cargarTareas(self):
        # Si la lista de tareas está vacía, cargamos las tareas inicialmente desde el archivo
        if len(self.tareas) == 0:
            try:
                with open('scrappers/gestion_tareas/tasks.txt', mode='r') as file:
                    for linea in file:
                        # Suponemos que el archivo tiene el formato: id|titulo|descripcion|completada
                        partes = linea.strip().split('|')
                        
                        if len(partes) == 4:
                            # Creamos un diccionario con los datos de la tarea
                            tarea = {
                                'id': int(partes[0]),  # Convierte el ID a entero
                                'titulo': partes[1],
                                'descripcion': partes[2],
                                'estado': partes[3].lower() == 'true'  # Convierte "True"/"False" a booleano
                            }
                            # Añadimos la tarea a la lista
                            self.tareas.append(tarea)
            except FileNotFoundError:
                print("El archivo no existe.")
            except Exception as e:
                print(f"Error al cargar las tareas: {e}")

    def actualizarArchivoTareas(self):
        try:
            with open('scrappers/gestion_tareas/tasks.txt', mode='w') as file:
                for tarea in self.tareas:
                    # Escribimos cada tarea en una línea del archivo
                    file.write(f"{tarea['id']}|{tarea['titulo']}|{tarea['descripcion']}|{str(tarea['estado'])}\n")
        except Exception as e:
            print(f"Error al actualizar el archivo: {e}")

    def verTareas(self):
        for t in self.tareas:
            print(f"ID: {t['id']} | Título: {t['titulo']} | Descripción: {t['descripcion']} | Completada: {t['estado']}")

    def marcarCompletada(self, id):
        for i in self.tareas:
            if i['id'] == id:
                i['estado'] = True
                print('Tarea Completada')
        self.actualizarArchivoTareas()