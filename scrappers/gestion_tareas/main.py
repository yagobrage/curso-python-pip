import tarea

def main():

    control = tarea.ControlTareas()

    control.añadirTarea({
        'id': 1,
        'titulo': 'MATES',
        'descripcion': 'Hacer sumas',
        'estado': False
    })

    control.verTareas()

    control.marcarCompletada(id=1)

    control.verTareas()

if __name__ == '__main__':
    main()