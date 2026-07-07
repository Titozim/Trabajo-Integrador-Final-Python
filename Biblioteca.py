from datetime import datetime

class usuario:
    def __init__(self, 
                 dni: int,
                 nombre_apellido: str,
                 celular: int,
                 fecha_registro: datetime,
                 direccion: str ):
        self.dni = dni #id de usuario
        self.nombre_apellido = nombre_apellido 
        self.celular = celular
        self.fecha_registro = fecha_registro
        self.direccion = direccion
        
class libros: 
    def __init__(self, 
                 nombre_libro: str, 
                 nombre_autor: str, 
                 cant_copias: int, 
                 disponbibilidad: bool):
        self.nombre_libro = nombre_libro #es el id de mi libro
        self.nombre_autor = nombre_autor
        self.cant_copias = cant_copias
        self.disponibilidad = disponbibilidad
            
class prestamo:
    def __init__(self,
                 dni: int,
                 nombre_libro : str,
                 fecha_prestamo : datetime,
                 fecha_vencimiento : datetime,
                 devuelto: bool,
                 fecha_devolucion: None):
        self.dni = dni
        self.nombre_libro = nombre_libro
        self.fecha_prestamo = fecha_prestamo
        self.fecha_vencimiento = fecha_vencimiento
        self.devuelto = devuelto
        self.fecha_devolucion = fecha_devolucion 
        
    def calcular_multa(self):
        if self.devuelto:
            fecha_referencia = self.fecha_devolucion
        else:
            fecha_referencia = datetime.now()

        if fecha_referencia > self.fecha_vencimiento:
            dias_retraso = (fecha_referencia - self.fecha_vencimiento).days
            return dias_retraso * 3500
        return 0
    
def registrar_usuario():
    print("\n--- Registro de Nuevo Usuario ---")
    
    # 1. Validación del DNI con bandera
    dni_valido = False
    while not dni_valido:
        try:
            dni = int(input("Ingrese DNI (sin puntos ni espacios): "))
            if dni > 0:
                dni_valido = True  # La bandera cambia, el bucle termina
            else:
                print("Error: El DNI debe ser mayor a cero.")
        except ValueError:
            print("Error: Ingrese únicamente números para el DNI.")

    # 2. Validación de Nombre y Apellido con bandera
    nombre_valido = False
    while not nombre_valido:
        nombre_apellido = input("Ingrese Nombre y Apellido: ").strip()
        if nombre_apellido != "":
            nombre_valido = True
        else:
            print("Error: Este campo no puede quedar vacío.")

    # 3. Validación del Celular con bandera
    celular_valido = False
    while not celular_valido:
        try:
            celular = int(input("Ingrese número de celular: "))
            if celular > 0:
                celular_valido = True
            else:
                print("Error: El celular debe ser un número válido.")
        except ValueError:
            print("Error: Ingrese únicamente números para el celular.")

    # Fecha de registro automática
    fecha_registro = datetime.now()

    # 4. Validación de Dirección con bandera
    direccion_valida = False
    while not direccion_valida:
        direccion = input("Ingrese Dirección: ").strip()
        if direccion != "":
            direccion_valida = True
        else:
            print("Error: La dirección no puede quedar vacía.")

    # Creación del objeto usuario
    nuevo_usuario = usuario(dni, nombre_apellido, celular, fecha_registro, direccion)
    print(f"\n¡Usuario '{nombre_apellido}' registrado con éxito!")
    
    return nuevo_usuario

def pedir_libro_prestado(nombre_archivo="libros.txt"):
    print("\n--- Solicitar Préstamo de Libro ---")
    
    # 1. Validación del nombre del libro (usando bandera, sin break)
    nombre_valido = False
    while not nombre_valido:
        libro_buscado = input("Ingrese el nombre del libro que desea pedir prestado: ").strip()
        if libro_buscado != "":
            nombre_valido = True
        else:
            print("Error: El nombre del libro no puede quedar vacío.")    
    
    # Variables de estado para controlar qué pasó durante la búsqueda
    libro_encontrado = False
    prestamo_exitoso = False
    lineas_actualizadas = []
    
    try:
        # 2. Leemos todo el archivo de texto y lo guardamos en memoria
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
    
    # 3. Recorremos línea por línea buscando el libro
        for linea in lineas:
            datos = linea.strip().split('|')
            
            # Verifico que la línea tenga el formato correcto (4 datos)
            if len(datos) == 4:
                nombre_libro = datos[0]
                nombre_autor = datos[1]
                cant_copias = int(datos[2])
                disponibilidad = datos[3].strip() == 'True'

                # Comparo ignorando mayúsculas/minúsculas usando .lower()
                if nombre_libro.lower() == libro_buscado.lower():
                    libro_encontrado = True
                    
                    # Verifico si hay stock
                    if cant_copias > 0 and disponibilidad:
                        cant_copias -= 1  # Descontamos 1
                        prestamo_exitoso = True
                        print(f"\n¡Éxito! Se ha registrado el préstamo de '{nombre_libro}'.")