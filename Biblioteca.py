from datetime import datetime, timedelta

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

#creo una clase biblioteca para que almacene todo en conjunto 
class Biblioteca:
    def __init__(self):
        self.libros = {}      # nombre_libro (lower) -> Libro
        self.usuarios = {}    # dni -> Usuario
        self.prestamos = []   # lista de Prestamo
        
        #ahora se realizan la carga de los libros 
    def cargar_libros(self, ruta_txt="libro.txt"):
        try:
            with open(ruta_txt, encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    datos = linea.split("|")
                    if len(datos) != 4:
                        print(f"línea mal formada, se ignora ... {linea}")
                        continue
                    nombre, autor, cant, disp = datos
                    libro = libro(nombre, autor, int(cant), disp.strip() == "True") #me lo recomendo claude (investigar si se puede hacer asi)
                    self.libros[nombre.lower()] = libro #la funcion lower me hace todo en minuscula
            print(f"Se cargaron {len(self.libros)} libros desde '{ruta_txt}'.")
        except FileNotFoundError:
            print(f"No se encontró el archivo '{ruta_txt}'.")

    def guardar_libros(self, ruta_txt="libro.txt"):
        try:
            with open(ruta_txt, "w", encoding="utf-8") as f:
                for libro in self.libros.values():
                    f.write(f"{libro.nombre_libro}|{libro.nombre_autor}|"
                            f"{libro.cant_copias}|{libro.disponibilidad}\n")
        except Exception as e:
            print(f"Ocurrió un error al guardar los libros: {e}")
            
    #---ahroa se realiza el registro de usuarios----
    
    def registrar_usuario(self):
        print("\n--- Registro de Nuevo Usuario ---") #informo 

        dni_valido = False
        while not dni_valido:
            try:
                dni = int(input("Ingrese DNI (sin puntos ni espacios): "))
                if dni > 0:
                    dni_valido = True
                else:
                    print("Error: El DNI debe ser mayor a cero.")
            except ValueError:
                print("Error: Ingrese únicamente números para el DNI.")

        if dni in self.usuarios:
            print("Ya existe un usuario registrado con ese DNI.")
            return self.usuarios[dni]

        nombre_valido = False
        while not nombre_valido:
            nombre_apellido = input("Ingrese Nombre y Apellido: ").strip()
            if nombre_apellido != "":
                nombre_valido = True
            else:
                print("Error: Este campo no puede quedar vacío.")

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

        fecha_registro = datetime.now()

        direccion_valida = False
        while not direccion_valida:
            direccion = input("Ingrese Dirección: ").strip()
            if direccion != "":
                direccion_valida = True
            else:
                print("Error: La dirección no puede quedar vacía.")

        nuevo_usuario = usuario(dni, nombre_apellido, celular, fecha_registro, direccion)
        self.usuarios[dni] = nuevo_usuario
        print(f"\n¡Usuario '{nombre_apellido}' registrado con éxito!")
        return nuevo_usuario

    #-- funcion para mostrar los libros que tengo---
    
    def mostrar_libros_disponibles(self):
        disponibles = [libro for libro in self.libros.values()
                       if libro.disponibilidad and libro.cant_copias > 0]
 
        if not disponibles:
            print("\nNo hay libros disponibles en este momento.")
            return disponibles
 
        print("\n--- Libros Disponibles ---")
        for libro in sorted(disponibles, key=lambda l: l.nombre_libro.lower()):
            print(f"- {libro.nombre_libro} | {libro.nombre_autor} | "
                  f"{libro.cant_copias} copia(s) disponible(s)")
        return disponibles
    
     #--- aca realizo el pedido de prestamo de libro--- 

    def prestar_libro(self, dni, nombre_libro, dias_prestamo=7):
        if dni not in self.usuarios:
            print("No existe un usuario registrado con ese DNI. Registrelo primero.")
            return None

        clave = nombre_libro.strip().lower()
        libro = self.libros.get(clave)

        if libro is None:
            print(f"No se encontró el libro '{nombre_libro}' en el catálogo.")
            return None

        if libro.cant_copias <= 0 or not libro.disponibilidad:
            print(f"Lo sentimos, no hay copias disponibles de '{libro.nombre_libro}'.")
            return None

        # Descontamos stock
        libro.cant_copias -= 1
        if libro.cant_copias == 0:
            libro.disponibilidad = False

        fecha_prestamo = datetime.now()
        fecha_vencimiento = fecha_prestamo + timedelta(days=dias_prestamo)

        nuevo_prestamo = prestamo(dni, libro.nombre_libro, fecha_prestamo, fecha_vencimiento)
        self.prestamos.append(nuevo_prestamo)

        self.guardar_libros()

        print(f"\nSe registró el préstamo de '{libro.nombre_libro}' "
              f"para el usuario {dni}. Vence el {fecha_vencimiento.strftime('%d/%m/%Y')}.") #claude me recomendo que escriba asi la fecha de vencimiento (verificar)
        return nuevo_prestamo
    
     # ---funcion para realizar la devolucion de los libros---
    def devolver_libro(self, dni, nombre_libro):
        clave = nombre_libro.strip().lower()

        prestamo_buscado = None
        for prestamo in self.prestamos:
            if (prestamo.dni == dni
                    and prestamo.nombre_libro.lower() == clave
                    and not prestamo.devuelto):
                prestamo_buscado = prestamo
                break

        if prestamo_buscado is None:
            print("No se encontró un préstamo activo con esos datos.")
            return None

        prestamo_buscado.devuelto = True
        prestamo_buscado.fecha_devolucion = datetime.now()

        libro = self.libros.get(clave)
        if libro is not None:
            libro.cant_copias += 1
            libro.disponibilidad = True
            self.guardar_libros()

        multa = prestamo_buscado.calcular_multa()
        if multa > 0:
            print(f"\nDevolución registrada. El usuario tiene una multa de ${multa} por demora.")
        else:
            print("\nDevolución registrada. Sin multas.")

        return prestamo_buscado

    # --- funcion para ver estadisticas ----
    def libro_mas_solicitado(self): 
        if not self.prestamos:
            print("Todavía no se registraron préstamos.")
            return None

        conteo = {}
        for prestamo in self.prestamos: #realizo un contador para contar cual es el nombre del libro que mas de pide 
            conteo[prestamo.nombre_libro] = conteo.get(prestamo.nombre_libro, 0) + 1

        libro_top = max(conteo, key=conteo.get) #recomendacion de claude para verificar con un valor alto para saber cual es el mayor 
        print(f"El libro más solicitado es '{libro_top}' con {conteo[libro_top]} préstamo(s).")
        return libro_top, conteo[libro_top]

    def cantidad_prestamos_realizados(self):
        total = len(self.prestamos)
        print(f"Cantidad total de préstamos realizados: {total}")
        return total
    
# creo un menu para poder realizar las acciones

def menu():
    biblioteca = Biblioteca()
    biblioteca.cargar_libros("libro.txt")
 
    opciones = {
        "1": "Registrar usuario",
        "2": "Ver libros disponibles",
        "3": "Pedir libro prestado",
        "4": "Devolver libro",
        "5": "Ver libro más solicitado",
        "6": "Ver cantidad de préstamos realizados",
        "7": "Salir",
    }
 
    while True:
        print("\n--- Sistema de Biblioteca ---")
        for clave, texto in opciones.items():
            print(f"{clave}. {texto}")
 
        opcion = input("Elija una opción: ").strip()
 
        if opcion == "1":
            biblioteca.registrar_usuario()
        elif opcion == "2":
            biblioteca.mostrar_libros_disponibles()
        elif opcion == "3":
            dni = int(input("Ingrese su DNI: "))
            nombre_libro = input("Ingrese el nombre del libro: ")
            biblioteca.prestar_libro(dni, nombre_libro)
        elif opcion == "4":
            dni = int(input("Ingrese su DNI: "))
            nombre_libro = input("Ingrese el nombre del libro a devolver: ")
            biblioteca.devolver_libro(dni, nombre_libro)
        elif opcion == "5":
            biblioteca.libro_mas_solicitado()
        elif opcion == "6":
            biblioteca.cantidad_prestamos_realizados()
        elif opcion == "7":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, intente de nuevo.")
 
 
if __name__ == "__main__":
    menu()