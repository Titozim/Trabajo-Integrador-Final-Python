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
            
class prestamo(usuario, libros):
    def __init__(self,
                 dni: int,
                 nombre_libro : str,
                 fecha_prestamo : datetime,
                 fecha_vencimiento : datetime,
                 devuelto: bool):
        self.dni = dni
        self.nombre_libro = nombre_libro
        self.fecha_prestamo = fecha_prestamo
        self.fecha_vencimiento = fecha_vencimiento
        self.devuelto = devuelto
        
        def calcular_multa(self):
            fecha_actual = datetime.now()
            
            if self.devuelto:
                if fecha_actual > self.fecha_vencimiento:
                    dias_retraso = (fecha_actual - self.fecha_vencimiento)
                    multa = dias_retraso * 3500
                    return multa
                else:
                    return 0
    