from datetime import datetime, timedelta


class Usuario:
    def __init__(self,
                 dni: int,
                 nombre_apellido: str,
                 celular: int,
                 fecha_registro: datetime,
                 direccion: str):
        self.dni = dni  # id de usuario
        self.nombre_apellido = nombre_apellido
        self.celular = celular
        self.fecha_registro = fecha_registro
        self.direccion = direccion


class Libro:
    def __init__(self,
                 nombre_libro: str,
                 nombre_autor: str,
                 cant_copias: int,
                 disponibilidad: bool):
        self.nombre_libro = nombre_libro  # id del libro
        self.nombre_autor = nombre_autor
        self.cant_copias = cant_copias
        self.disponibilidad = disponibilidad


class Prestamo:
    def __init__(self,
                 dni: int,
                 nombre_libro: str,
                 fecha_prestamo: datetime,
                 fecha_vencimiento: datetime,
                 devuelto: bool = False,
                 fecha_devolucion: datetime = None):
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


class Biblioteca:
    def __init__(self):
        self.libros = {}      # nombre_libro (lower) -> Libro
        self.usuarios = {}    # dni -> Usuario
        self.prestamos = []   # lista de Prestamo

    # ---------- CARGA DE LIBROS DESDE TXT ----------
    def cargar_libros(self, ruta_txt="libro.txt"):
        try:
            with open(ruta_txt, encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    datos = linea.split("|")
                    if len(datos) != 4:
                        print(f"Aviso: línea mal formada, se ignora -> {linea}")
                        continue
                    nombre, autor, cant, disp = datos
                    libro = Libro(nombre, autor, int(cant), disp.strip() == "True")
                    self.libros[nombre.lower()] = libro
            print(f"Se cargaron {len(self.libros)} libros desde '{ruta_txt}'.")
        except FileNotFoundError:
            print(f"No se encontró el archivo '{ruta_txt}'.")

    def guardar_libros(self, ruta_txt="libro.txt"):
        if not self.libros:
            print("Aviso: el catálogo en memoria está vacío, no se sobrescribe el archivo.")
            return
        try:
            with open(ruta_txt, "w", encoding="utf-8") as f:
                for libro in self.libros.values():
                    f.write(f"{libro.nombre_libro}|{libro.nombre_autor}|"
                            f"{libro.cant_copias}|{libro.disponibilidad}\n")
        except Exception as e:
            print(f"Ocurrió un error al guardar los libros: {e}")

    # ---------- REGISTRO DE USUARIOS ----------
    def registrar_usuario(self):
        print("\n--- Registro de Nuevo Usuario ---")

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

        nuevo_usuario = Usuario(dni, nombre_apellido, celular, fecha_registro, direccion)
        self.usuarios[dni] = nuevo_usuario
        print(f"\n¡Usuario '{nombre_apellido}' registrado con éxito!")
        return nuevo_usuario

    # ---------- CONSULTA DE CATÁLOGO ----------
    def mostrar_catalogo(self):
        if not self.libros:
            print("\nNo hay libros cargados en el catálogo.")
            return

        print("\n--- Catálogo de Libros ---")
        for libro in sorted(self.libros.values(), key=lambda l: l.nombre_libro.lower()):
            print(f"- {libro.nombre_libro}")

    # ---------- PRÉSTAMOS ----------
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

        nuevo_prestamo = Prestamo(dni, libro.nombre_libro, fecha_prestamo, fecha_vencimiento)
        self.prestamos.append(nuevo_prestamo)

        self.guardar_libros()

        print(f"\n¡Éxito! Se registró el préstamo de '{libro.nombre_libro}' "
              f"para el usuario {dni}. Vence el {fecha_vencimiento.strftime('%d/%m/%Y')}.")
        return nuevo_prestamo

    # ---------- DEVOLUCIONES ----------
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

    # ---------- SIMULACIÓN DE ATRASO (SOLO PARA PRUEBAS) ----------
    def simular_atraso(self, dni, nombre_libro, dias_atraso):
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

        prestamo_buscado.fecha_vencimiento -= timedelta(days=dias_atraso)
        print(f"\nSe adelantó el vencimiento {dias_atraso} día(s) para poder probar el cálculo de multas.")
        print(f"Nueva fecha de vencimiento: {prestamo_buscado.fecha_vencimiento.strftime('%d/%m/%Y')}")
        return prestamo_buscado
    def libro_mas_solicitado(self):
        if not self.prestamos:
            print("Todavía no se registraron préstamos.")
            return None

        conteo = {}
        for prestamo in self.prestamos:
            conteo[prestamo.nombre_libro] = conteo.get(prestamo.nombre_libro, 0) + 1

        libro_top = max(conteo, key=conteo.get)
        print(f"El libro más solicitado es '{libro_top}' con {conteo[libro_top]} préstamo(s).")
        return libro_top, conteo[libro_top]

    def cantidad_prestamos_realizados(self):
        total = len(self.prestamos)
        print(f"Cantidad total de préstamos realizados: {total}")
        return total


# ---------- MENÚ DE USO ----------
def menu():
    biblioteca = Biblioteca()
    biblioteca.cargar_libros("libro.txt")

    opciones = {
        "1": "Registrar usuario",
        "2": "Ver catálogo de libros",
        "3": "Pedir libro prestado",
        "4": "Devolver libro",
        "5": "Ver libro más solicitado",
        "6": "Ver cantidad de préstamos realizados",
        "7": "Simular atraso (solo para pruebas de multas)",
        "8": "Salir",
    }

    while True:
        print("\n--- Sistema de Biblioteca ---")
        for clave, texto in opciones.items():
            print(f"{clave}. {texto}")

        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            biblioteca.registrar_usuario()
        elif opcion == "2":
            biblioteca.mostrar_catalogo()
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
            dni = int(input("Ingrese el DNI del préstamo a atrasar: "))
            nombre_libro = input("Ingrese el nombre del libro: ")
            dias = int(input("¿Cuántos días de atraso querés simular?: "))
            biblioteca.simular_atraso(dni, nombre_libro, dias)
        elif opcion == "8":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    menu()