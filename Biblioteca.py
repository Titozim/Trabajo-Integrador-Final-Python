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

    