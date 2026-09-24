# PROYECTO FINAL: SISTEMA DE INVENTARIO DE SR. PALOMO
# Programa sencillo para registrar productos y ventas.
# El sistema está hecho con Python y Tkinter.

#Codigo para registro de productos de la tienda en linea de Sr.Palomo.
#Creacion del codigo: 20/08/2026. Hecha por Julio.
#Modificacion numero 1 (Empezar con la organización del código, crear la base del sistema): 28 y 29 de agosto de 2026. Hecha por Ronn.
#Modificacion numero 2 (Agregar funcionalidad para registrar ventas): 31 de agosto y 1 de septiembre de 2026. Hecha por Ronn.
#Modificacion numero 3 (Agregar funcionalidad para registrar productos): 17/09/2026. Hecha por Julio.
#Modificacion numero 4 (Debugging, arreglar errores del código): 22/09/2026. Hecha por Ronn.
#Modificación número 5 (Mejoras en la interfaz de usuario y muchas más funciones añadidas): 24/09/2026. Hecha por Oscar.

# -------------------- LIBRERÍAS --------------------

# Tkinter permite crear la ventana y los botones del programa.
import tkinter as tk

# ttk agrega elementos como listas desplegables, entradas y tablas.
from tkinter import ttk

# json permite guardar la información del programa en un archivo.
import json

# os permite construir correctamente la ubicación de la imagen.
import os

# datetime permite guardar la fecha y hora de cada venta.
from datetime import datetime


# -------------------- DATOS DEL PROGRAMA --------------------

# Se obtiene la carpeta donde está guardado el programa.
CARPETA = os.path.dirname(os.path.abspath(__file__))

# Se establece la ruta completa del archivo JSON.
ARCHIVO = os.path.join(CARPETA, "productos_sr_palomo.json")

# Nombre de la imagen que se mostrará dentro de la ventana principal.
IMAGEN = "sr_palomo_logo.png"

# Lista donde se almacenan todos los productos.
productos = []

# Lista donde se almacenan todas las ventas realizadas.
ventas = []

# Número que tendrá el siguiente producto que se registre.
siguiente_id = 1


# -------------------- GUARDAR Y CARGAR --------------------

# Esta función guarda todos los datos para que no se pierdan al cerrar el programa.
def guardar_datos():

    # Se crea un diccionario con las tres cosas que necesitamos guardar.
    datos = {
        "productos": productos,
        "ventas": ventas,
        "siguiente_id": siguiente_id
    }

    # Se abre el archivo en modo escritura.
    # "w" significa que se escribirá la información nueva.
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:

        # json.dump convierte el diccionario en información que se puede guardar.
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


# Esta función recupera los datos que ya estaban guardados al iniciar el programa.
def cargar_datos():

    # Estas variables son globales porque vamos a cambiar las listas originales.
    global productos, ventas, siguiente_id

    # Se intenta abrir el archivo donde están guardados los datos.
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:

            # json.load convierte la información del archivo nuevamente en datos de Python.
            datos = json.load(archivo)

        # Se recupera la lista de productos.
        productos = datos.get("productos", [])

        # Se recupera la lista de ventas.
        ventas = datos.get("ventas", [])

        # Se recupera el número para el siguiente producto.
        siguiente_id = datos.get("siguiente_id", 1)

        # Se revisa cada producto por si le falta algún dato de versiones anteriores.
        for producto in productos:

            # Si no existe "activo", se considera que el producto sigue activo.
            producto.setdefault("activo", True)

            # Si no existe "vendidos", comienza en cero.
            producto.setdefault("vendidos", 0)

            # Si no existe "ingresos", comienza en cero.
            producto.setdefault("ingresos", 0)

            # Si no existe "ganancia", comienza en cero.
            producto.setdefault("ganancia", 0)

    # Si el archivo todavía no existe o está dañado, se comienza con listas vacías.
    except (FileNotFoundError, json.JSONDecodeError):

        # Se reinicia la lista de productos.
        productos = []

        # Se reinicia la lista de ventas.
        ventas = []

        # El primer producto volverá a utilizar el ID 1.
        siguiente_id = 1


# Busca un producto usando el número de ID.
def buscar_producto(identificador):

    # Se recorren todos los productos uno por uno.
    for producto in productos:

        # Si el ID del producto coincide con el ID que buscamos...
        if producto["id"] == identificador:

            # ...se devuelve ese producto.
            return producto

    # Si no se encontró ningún producto, se devuelve None.
    return None


# Devuelve solamente los productos que todavía están activos.
def productos_activos():

    # Se revisan todos los productos y se conservan los que estén activos.
    return [p for p in productos if p.get("activo", True)]


# Convierte un número en una cantidad con formato de dinero.
def dinero(cantidad):

    # :.2f hace que siempre aparezcan dos números después del punto decimal.
    return f"${cantidad:.2f}"


# Calcula el nivel de demanda según las unidades vendidas.
def demanda(producto):

    # Si se vendieron 100 o más unidades, la demanda se considera alta.
    if producto["vendidos"] >= 100:
        return "Alta"

    # Si se vendieron 50 o más, pero menos de 100, se considera media.
    elif producto["vendidos"] >= 50:
        return "Media"

    # Cualquier cantidad menor a 50 se considera demanda baja.
    return "Baja"


# -------------------- INICIO DE SESIÓN --------------------

# Esta función crea una pantalla sencilla para pedir usuario y contraseña.
def iniciar_sesion():

    # Se crea la ventana principal del inicio de sesión.
    ventana_login = tk.Tk()

    # Se establece el título que aparece arriba de la ventana.
    ventana_login.title("Sr. Palomo - Inicio de sesión")

    # Se define el tamaño de la ventana de acceso.
    ventana_login.geometry("430x400")

    # Se evita que el usuario cambie el tamaño de la ventana.
    ventana_login.resizable(False, False)

    # Se coloca el color de fondo de la pantalla de acceso.
    ventana_login.configure(bg="#fff4e6")

    # Se obtiene la ubicación de la carpeta donde está este archivo Python.
    carpeta = os.path.dirname(os.path.abspath(__file__))

    # Se construye la ruta completa de la imagen.
    ruta_imagen = os.path.join(carpeta, IMAGEN)

    # Se carga la imagen proporcionada por el usuario.
    logo = tk.PhotoImage(file=ruta_imagen)

    # La imagen original es más grande que lo necesario.
    # subsample la reduce para mostrarla como un pequeño logotipo.
    logo = logo.subsample(4, 4)

    # Se guarda la imagen dentro de la ventana para que Tkinter no la elimine.
    ventana_login.logo = logo

    # Se coloca la imagen en la parte superior de la pantalla.
    tk.Label(
        ventana_login,
        image=logo,
        bg="#fff4e6"
    ).pack(pady=(12, 4))

    # Se coloca el nombre del negocio debajo de la imagen.
    tk.Label(
        ventana_login,
        text="SR. PALOMO",
        bg="#fff4e6",
        fg="#7a4300",
        font=("Arial", 20, "bold")
    ).pack(pady=3)

    # Se coloca una indicación para el usuario.
    tk.Label(
        ventana_login,
        text="Inicia sesión para entrar al sistema",
        bg="#fff4e6",
        fg="#8a6a4a",
        font=("Arial", 10)
    ).pack(pady=(0, 12))

    # Se crea una etiqueta para indicar dónde escribir el usuario.
    tk.Label(
        ventana_login,
        text="Usuario",
        bg="#fff4e6",
        fg="#7a4300",
        font=("Arial", 10, "bold")
    ).pack()

    # Se crea la caja donde se escribirá el usuario.
    entrada_usuario = ttk.Entry(ventana_login, width=28)

    # Se coloca la caja debajo de su etiqueta.
    entrada_usuario.pack(pady=5)

    # Se crea una etiqueta para indicar dónde escribir la contraseña.
    tk.Label(
        ventana_login,
        text="Contraseña",
        bg="#fff4e6",
        fg="#7a4300",
        font=("Arial", 10, "bold")
    ).pack(pady=(5, 0))

    # Se crea la caja para la contraseña.
    # show="*" evita que la contraseña aparezca directamente en pantalla.
    entrada_contrasena = ttk.Entry(
        ventana_login,
        width=28,
        show="*"
    )

    # Se coloca la caja debajo de la etiqueta.
    entrada_contrasena.pack(pady=5)

    # Esta etiqueta comenzará vacía y después mostrará errores de acceso.
    mensaje = tk.Label(
        ventana_login,
        text="",
        bg="#fff4e6",
        fg="#c0392b",
        font=("Arial", 9)
    )

    # Se coloca el mensaje debajo de las cajas.
    mensaje.pack(pady=5)

    # Esta función comprueba si los datos escritos son correctos.
    def comprobar():

        # Se obtiene el texto que escribió el usuario.
        usuario = entrada_usuario.get()

        # Se obtiene el texto que escribió en la contraseña.
        contrasena = entrada_contrasena.get()

        # Se comparan los datos con el usuario y contraseña establecidos.
        if usuario == "admin" and contrasena == "1234":

            # Si son correctos, se cierra la pantalla de inicio de sesión.
            ventana_login.destroy()

            # Después se abre el programa principal.
            abrir_programa()

        # Si alguno de los datos es incorrecto...
        else:

            # ...se muestra el error dentro de la misma ventana.
            mensaje.config(text="Usuario o contraseña incorrectos.")

    # Se crea el botón que ejecuta la comprobación.
    tk.Button(
        ventana_login,
        text="Iniciar sesión",
        command=comprobar,
        bg="#ff9c1d",
        fg="white",
        activebackground="#ff9c1d",
        activeforeground="white",
        relief="flat",
        bd=0,
        font=("Arial", 10, "bold"),
        padx=18,
        pady=7
    ).pack(pady=8)

    # El cursor comienza directamente en la caja de usuario.
    entrada_usuario.focus()

    # Enter también puede utilizarse para iniciar sesión.
    ventana_login.bind("<Return>", lambda evento: comprobar())

    # Se mantiene abierta la ventana hasta que el usuario inicie sesión.
    ventana_login.mainloop()


# -------------------- PROGRAMA PRINCIPAL --------------------

# Esta clase contiene la ventana y las funciones principales del inventario.
class Programa:

    # Este método se ejecuta cuando se crea el programa.
    def __init__(self, ventana):

        # Se guarda la ventana dentro de la clase para poder usarla después.
        self.ventana = ventana

        # Se cambia el título que aparece en la parte superior.
        self.ventana.title("Sr. Palomo - Inventario")

        # Se establece el tamaño de la ventana principal.
        self.ventana.geometry("1050x650")

        # Se impide que la ventana cambie de tamaño.
        self.ventana.resizable(False, False)

        # Se coloca el color de fondo general.
        self.ventana.configure(bg="#fff4e6")

        # Se crea un estilo sencillo para las tablas.
        estilo = ttk.Style()

        # Se utiliza el tema clam para que los controles tengan una apariencia simple.
        estilo.theme_use("clam")

        # Se establece el tamaño de las filas de las tablas.
        estilo.configure(
            "Treeview",
            rowheight=26,
            font=("Arial", 10)
        )

        # Se establece el estilo de los títulos de las tablas.
        estilo.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        # Se crea la parte superior de color naranja.
        encabezado = tk.Frame(
            ventana,
            bg="#ff9c1d",
            height=70
        )

        # El encabezado ocupa todo el ancho.
        encabezado.pack(fill="x")

        # Se evita que el contenido cambie la altura establecida.
        encabezado.pack_propagate(False)

        # Se obtiene la carpeta donde se encuentra el programa.
        carpeta = os.path.dirname(os.path.abspath(__file__))

        # Se obtiene la ruta de la imagen del negocio.
        ruta_imagen = os.path.join(carpeta, IMAGEN)

        # Se carga la imagen principal.
        self.logo = tk.PhotoImage(file=ruta_imagen)

        # Se reduce la imagen para que pueda aparecer en el encabezado.
        self.logo = self.logo.subsample(4, 4)

        # Se coloca la imagen dentro del encabezado.
        tk.Label(
            encabezado,
            image=self.logo,
            bg="#ff9c1d"
        ).pack(side="left", padx=10)

        # Se coloca el nombre del negocio en el encabezado.
        tk.Label(
            encabezado,
            text="SR. PALOMO",
            font=("Arial", 21, "bold"),
            bg="#ff9c1d",
            fg="white"
        ).pack(side="left", padx=10)

        # Se coloca una descripción corta junto al nombre.
        tk.Label(
            encabezado,
            text="Inventario Anime / K-Pop",
            font=("Arial", 12),
            bg="#ff9c1d",
            fg="white"
        ).pack(side="left")

        # Se crea el cuerpo principal debajo del encabezado.
        cuerpo = tk.Frame(
            ventana,
            bg="#fff4e6"
        )

        # El cuerpo ocupa todo el espacio disponible.
        cuerpo.pack(fill="both", expand=True)

        # Se crea el menú lateral.
        menu = tk.Frame(
            cuerpo,
            bg="#7a4300",
            width=190
        )

        # El menú ocupa toda la altura de la ventana.
        menu.pack(side="left", fill="y")

        # Se mantiene el ancho establecido.
        menu.pack_propagate(False)

        # Estas son las opciones que permanecen visibles en el menú lateral.
        opciones = [
            ("Inicio", self.inicio),
            ("Análisis de demanda", self.analisis_demanda),
            ("Resumen general", self.resumen_general),
            ("Historial de ventas", self.historial_ventas)
        ]

        # Se recorre cada opción para crear su botón.
        for texto, funcion in opciones:

            # Se crea un botón para cada opción del menú.
            tk.Button(
                menu,
                text=texto,
                command=funcion,
                bg="#7a4300",
                fg="white",
                activebackground="#7a4300",
                activeforeground="white",
                relief="flat",
                bd=0,
                font=("Arial", 10),
                anchor="w",
                padx=15,
                pady=8
            ).pack(fill="x")

        # Este marco es donde se mostrará cada sección del programa.
        self.contenido = tk.Frame(
            cuerpo,
            bg="#fff4e6"
        )

        # Se coloca a la derecha del menú y ocupa el espacio restante.
        self.contenido.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Se crea una barra inferior para mostrar mensajes sencillos.
        self.estado = tk.Label(
            ventana,
            text="",
            bg="#ffe0b3",
            fg="#7a4300",
            anchor="w",
            padx=10,
            pady=5
        )

        # La barra ocupa todo el ancho inferior.
        self.estado.pack(fill="x", side="bottom")

        # Al abrir el programa se muestra la pantalla de Inicio.
        self.inicio()

    # Borra todos los elementos de la sección anterior.
    def limpiar(self):

        # Se obtiene cada elemento que existe dentro del área de contenido.
        for elemento in self.contenido.winfo_children():

            # Se elimina ese elemento de la pantalla.
            elemento.destroy()

    # Coloca un título y, si existe, una descripción.
    def titulo(self, texto, descripcion=""):

        # Se crea la etiqueta principal con el título.
        tk.Label(
            self.contenido,
            text=texto,
            bg="#fff4e6",
            fg="#7a4300",
            font=("Arial", 19, "bold")
        ).pack(anchor="w", pady=(0, 4))

        # Solo se crea la descripción si se recibió algún texto.
        if descripcion:

            # Se muestra una explicación debajo del título.
            tk.Label(
                self.contenido,
                text=descripcion,
                bg="#fff4e6",
                fg="#8a6a4a",
                font=("Arial", 10)
            ).pack(anchor="w", pady=(0, 12))

    # Crea botones con el mismo diseño para no repetir toda su configuración.
    def boton(self, padre, texto, funcion, color="#ff9c1d"):

        # Se devuelve el botón ya configurado.
        return tk.Button(
            padre,
            text=texto,
            command=funcion,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=7
        )

    # Cambia el texto de la barra inferior para mostrar mensajes.
    def mensaje(self, texto):

        # config modifica el texto de la etiqueta que ya existe.
        self.estado.config(text=texto)

    # Actualiza la información básica que aparece abajo.
    def actualizar_estado(self):

        # Se obtiene solamente la lista de productos activos.
        lista = productos_activos()

        # Se cuentan los productos que tienen 10 unidades o menos.
        bajos = sum(
            1 for p in lista
            if p["inventario"] <= 10
        )

        # Se muestra la cantidad de productos y las alertas.
        self.estado.config(
            text=f"Productos: {len(lista)}   |   Inventario bajo: {bajos}"
        )

    # -------------------- INICIO --------------------

    # Esta función construye la pantalla principal del sistema.
    def inicio(self):

        # Primero se limpia lo que estuviera mostrado anteriormente.
        self.limpiar()

        # Se coloca el título de la pantalla.
        self.titulo(
            "Bienvenido a Sr. Palomo",
            "Sistema de gestión de inventario"
        )

        # Se obtiene la lista de productos que están activos.
        lista = productos_activos()

        # Se calculan los cuatro datos que aparecerán como resumen.
        datos = [
            ("Productos", len(lista)),
            ("Unidades vendidas", sum(p["vendidos"] for p in lista)),
            ("Ingresos", dinero(sum(p["ingresos"] for p in lista))),
            ("Ganancias", dinero(sum(p["ganancia"] for p in lista)))
        ]

        # Se crea el espacio que contendrá las tarjetas.
        tarjetas = tk.Frame(
            self.contenido,
            bg="#fff4e6"
        )
        tarjetas.pack(fill="x", pady=10)

        # Se recorre cada dato para crear una tarjeta.
        for i, (nombre, valor) in enumerate(datos):

            # Se crea una tarjeta de color claro.
            tarjeta = tk.Frame(
                tarjetas,
                bg="#ffe0b3",
                padx=15,
                pady=15
            )

            # Se coloca la tarjeta en una columna.
            tarjeta.grid(
                row=0,
                column=i,
                padx=4,
                sticky="nsew"
            )

            # Se permite que las columnas ocupen el espacio disponible.
            tarjetas.grid_columnconfigure(i, weight=1)

            # Se muestra el nombre del dato.
            tk.Label(
                tarjeta,
                text=nombre,
                bg="#ffe0b3",
                fg="#7a4300"
            ).pack()

            # Se muestra el valor del dato.
            tk.Label(
                tarjeta,
                text=str(valor),
                bg="#ffe0b3",
                fg="#7a4300",
                font=("Arial", 16, "bold")
            ).pack(pady=5)

        # Este título separa el resumen de los accesos principales.
        tk.Label(
            self.contenido,
            text="Accesos rápidos",
            bg="#fff4e6",
            fg="#7a4300",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=15)

        # Este botón es el único acceso para registrar productos.
        self.boton(
            self.contenido,
            "Registrar producto",
            self.registrar_producto
        ).pack(anchor="w", pady=4)

        # Este botón es el único acceso para registrar ventas.
        self.boton(
            self.contenido,
            "Registrar venta",
            self.registrar_venta,
            "#2874a6"
        ).pack(anchor="w", pady=4)

        # Este botón es el único acceso para consultar el inventario.
        self.boton(
            self.contenido,
            "Ver inventario",
            self.inventario,
            "#148f77"
        ).pack(anchor="w", pady=4)

        # Se actualiza la barra inferior.
        self.actualizar_estado()

    # -------------------- PRODUCTOS --------------------

    # Esta función crea el formulario para registrar o modificar productos.
    def formulario_producto(self, producto=None):

        # Se limpia la pantalla anterior.
        self.limpiar()

        # Si producto no es None, significa que estamos modificando.
        editar = producto is not None

        # Se muestra un título diferente dependiendo de la acción.
        if editar:
            self.titulo("Modificar producto")
        else:
            self.titulo("Registrar producto")

        # Se crea el espacio blanco del formulario.
        formulario = tk.Frame(
            self.contenido,
            bg="white",
            padx=20,
            pady=15
        )
        formulario.pack(fill="x", anchor="n")

        # Diccionario donde se guardarán las cajas de texto.
        campos = {}

        # Lista con los nombres de los campos y la clave que tendrán.
        etiquetas = [
            ("Nombre", "nombre"),
            ("Franquicia / Anime o serie", "franquicia"),
            ("Tipo de producto", "tipo"),
            ("Precio de venta", "precio"),
            ("Costo de producción", "costo"),
            ("Cantidad en inventario", "inventario")
        ]

        # Se recorren los campos para crear sus etiquetas y cajas.
        for fila, (texto, clave) in enumerate(etiquetas):

            # Se crea el texto que indica qué debe escribirse.
            tk.Label(
                formulario,
                text=texto,
                bg="white",
                fg="#7a4300",
                font=("Arial", 10, "bold")
            ).grid(
                row=fila,
                column=0,
                sticky="w",
                pady=7
            )

            # Se crea la caja donde se escribirá el dato.
            entrada = ttk.Entry(
                formulario,
                width=35
            )

            # Se coloca la caja junto a su etiqueta.
            entrada.grid(
                row=fila,
                column=1,
                sticky="w",
                pady=7
            )

            # Se guarda la caja en el diccionario usando su nombre.
            campos[clave] = entrada

        # Se crea la etiqueta de categoría.
        tk.Label(
            formulario,
            text="Categoría",
            bg="white",
            fg="#7a4300",
            font=("Arial", 10, "bold")
        ).grid(
            row=0,
            column=2,
            padx=15
        )

        # Se crea una lista desplegable para escoger Anime o K-Pop.
        categoria = ttk.Combobox(
            formulario,
            values=["Anime", "K-Pop"],
            state="readonly",
            width=15
        )

        # Se coloca la lista desplegable.
        categoria.grid(row=0, column=3)

        # Anime queda seleccionado por defecto.
        categoria.set("Anime")

        # Si estamos modificando un producto, se cargan sus datos anteriores.
        if editar:

            # Se recorre cada campo existente.
            for clave in campos:

                # Se escribe el dato anterior dentro de su caja.
                campos[clave].insert(
                    0,
                    str(producto.get(clave, ""))
                )

            # Se selecciona la categoría anterior.
            categoria.set(
                producto.get("categoria", "Anime")
            )

        # Esta función toma los datos escritos y los guarda.
        def guardar():

            # Se indica que vamos a modificar el ID general.
            global siguiente_id

            # Se obtiene el nombre y se quitan espacios al inicio y al final.
            nombre = campos["nombre"].get().strip()

            # Se obtiene la franquicia y se quitan espacios innecesarios.
            franquicia = campos["franquicia"].get().strip()

            # Se obtiene el tipo de producto.
            tipo = campos["tipo"].get().strip()

            # Si falta alguno de los datos principales, se muestra un mensaje.
            if not nombre or not franquicia or not tipo:
                self.mensaje(
                    "Faltan datos. Completa los campos de texto."
                )
                return

            # Se intenta convertir precio, costo y cantidad a números.
            try:

                # float permite usar números con decimales para el precio.
                precio = float(
                    campos["precio"].get().replace(",", ".")
                )

                # float también permite decimales para el costo.
                costo = float(
                    campos["costo"].get().replace(",", ".")
                )

                # int obliga a que la cantidad sea un número entero.
                cantidad = int(
                    campos["inventario"].get()
                )

                # No se permiten valores negativos.
                if precio < 0 or costo < 0 or cantidad < 0:
                    raise ValueError

            # Si alguna conversión falla, se muestra el mensaje correspondiente.
            except ValueError:
                self.mensaje(
                    "Revisa precio, costo y cantidad. Deben ser números válidos."
                )
                return

            # El precio de venta no puede ser menor al costo.
            if precio < costo:
                self.mensaje(
                    "El precio de venta no puede ser menor que el costo."
                )
                return

            # Se agrupan los datos del producto en un solo diccionario.
            datos = {
                "nombre": nombre,
                "categoria": categoria.get(),
                "franquicia": franquicia,
                "tipo": tipo,
                "precio": precio,
                "costo": costo,
                "inventario": cantidad
            }

            # Si estamos editando, se actualiza el producto existente.
            if editar:

                # update reemplaza los datos anteriores por los nuevos.
                producto.update(datos)

                # Se prepara el mensaje que se mostrará al terminar.
                texto = "Producto modificado."

            # Si no estamos editando, se crea un producto nuevo.
            else:

                # copy crea una copia de los datos básicos.
                nuevo = datos.copy()

                # Se asigna el ID actual al nuevo producto.
                nuevo["id"] = siguiente_id

                # Un producto nuevo comienza con cero ventas.
                nuevo["vendidos"] = 0

                # Un producto nuevo comienza con cero ingresos.
                nuevo["ingresos"] = 0

                # Un producto nuevo comienza con cero de ganancia.
                nuevo["ganancia"] = 0

                # True significa que aparece como producto activo.
                nuevo["activo"] = True

                # Se agrega el producto a la lista.
                productos.append(nuevo)

                # Se aumenta el número para el siguiente producto.
                siguiente_id += 1

                # Se prepara el mensaje de confirmación.
                texto = f"Producto registrado con ID {nuevo['id']}."

            # Se guardan los cambios en el archivo.
            guardar_datos()

            # Después de guardar, se regresa al inventario.
            self.inventario()

            # Se muestra el resultado en la barra inferior.
            self.mensaje(texto)

        # Botón que guarda el producto.
        self.boton(
            self.contenido,
            "Guardar",
            guardar
        ).pack(anchor="w", pady=12)

        # Botón que cancela y regresa al inventario.
        self.boton(
            self.contenido,
            "Cancelar",
            self.inventario,
            "#7f8c8d"
        ).pack(anchor="w")

    # Abre el formulario vacío para registrar un producto.
    def registrar_producto(self):

        # None indica que no se está modificando ningún producto.
        self.formulario_producto()

    # Permite elegir un producto de una lista antes de realizar una acción.
    def seleccionar_en_pantalla(self, titulo, funcion):

        # Se obtiene solamente la lista de productos activos.
        lista = productos_activos()

        # Se limpia la pantalla actual.
        self.limpiar()

        # Se coloca el título de la acción.
        self.titulo(
            titulo,
            "Selecciona un producto de la lista."
        )

        # Si no hay productos, se informa al usuario.
        if not lista:

            # Se muestra el mensaje dentro de la ventana.
            tk.Label(
                self.contenido,
                text="No hay productos registrados.",
                bg="#fff4e6",
                fg="#7a4300"
            ).pack(anchor="w", pady=10)

            # Se detiene la función porque no hay nada que seleccionar.
            return

        # Se crea una lista de texto para mostrar cada producto.
        opciones = [
            f"ID {p['id']} - {p['nombre']}"
            for p in lista
        ]

        # Se crea una lista desplegable con los productos.
        combo = ttk.Combobox(
            self.contenido,
            values=opciones,
            state="readonly",
            width=45
        )

        # Se coloca la lista en la pantalla.
        combo.pack(anchor="w", pady=8)

        # Se selecciona automáticamente el primer producto.
        combo.current(0)

        # Esta función se ejecuta cuando se presiona Continuar.
        def continuar():

            # Se obtiene el producto correspondiente a la opción seleccionada.
            producto = lista[combo.current()]

            # Se llama a la función que se recibió como parámetro.
            funcion(producto)

        # Se crea el botón para continuar con el producto elegido.
        self.boton(
            self.contenido,
            "Continuar",
            continuar
        ).pack(anchor="w", pady=8)

    # Permite elegir un producto y abrirlo para modificar.
    def modificar_producto(self):

        # Se muestra la lista y después se abre el formulario.
        self.seleccionar_en_pantalla(
            "Modificar producto",
            self.formulario_producto
        )

    # Permite elegir un producto y quitarlo del inventario activo.
    def eliminar_producto(self):

        # Esta función realiza la baja del producto elegido.
        def eliminar(producto):

            # False hace que el producto deje de aparecer como activo.
            producto["activo"] = False

            # Se guardan los cambios.
            guardar_datos()

            # Se regresa al inventario.
            self.inventario()

            # Se informa lo que ocurrió.
            self.mensaje(
                "Producto eliminado del inventario."
            )

        # Primero se muestra la lista de productos.
        self.seleccionar_en_pantalla(
            "Eliminar producto",
            eliminar
        )

    # -------------------- INVENTARIO --------------------

    # Esta función muestra todos los productos activos en una tabla.
    def inventario(self):

        # Se limpia la pantalla anterior.
        self.limpiar()

        # Se coloca el título de inventario.
        self.titulo("Inventario")

        # Se crea un espacio para el filtro de categoría.
        controles = tk.Frame(
            self.contenido,
            bg="#fff4e6"
        )
        controles.pack(
            fill="x",
            pady=(0, 8)
        )

        # Se coloca la etiqueta del filtro.
        tk.Label(
            controles,
            text="Categoría:",
            bg="#fff4e6",
            fg="#7a4300"
        ).pack(side="left")

        # Se crea la lista para elegir Todas, Anime o K-Pop.
        filtro = ttk.Combobox(
            controles,
            values=["Todas", "Anime", "K-Pop"],
            state="readonly",
            width=10
        )

        # Se selecciona Todas al comenzar.
        filtro.set("Todas")

        # Se coloca el filtro junto a su etiqueta.
        filtro.pack(
            side="left",
            padx=7
        )

        # Estas son las columnas que tendrá la tabla.
        columnas = (
            "id",
            "nombre",
            "categoria",
            "franquicia",
            "tipo",
            "precio",
            "costo",
            "inventario",
            "vendidos"
        )

        # Se crea la tabla utilizando esas columnas.
        tabla = ttk.Treeview(
            self.contenido,
            columns=columnas,
            show="headings"
        )

        # Estos son los nombres que verá el usuario.
        encabezados = [
            "ID",
            "Nombre",
            "Categoría",
            "Franquicia",
            "Tipo",
            "Precio",
            "Costo",
            "Stock",
            "Vendidos"
        ]

        # Se configura cada columna con su título.
        for columna, texto in zip(columnas, encabezados):

            # Se coloca el texto del encabezado.
            tabla.heading(
                columna,
                text=texto
            )

            # Se define el ancho y la alineación.
            tabla.column(
                columna,
                width=100,
                anchor="center"
            )

        # Se muestra la tabla.
        tabla.pack(
            fill="both",
            expand=True
        )

        # Esta función llena la tabla con los productos actuales.
        def llenar():

            # Primero se borran los registros que ya estaban en la tabla.
            tabla.delete(
                *tabla.get_children()
            )

            # Se obtiene la lista de productos activos.
            lista = productos_activos()

            # Si se eligió una categoría específica...
            if filtro.get() != "Todas":

                # ...se conservan solamente los productos de esa categoría.
                lista = [
                    p for p in lista
                    if p["categoria"] == filtro.get()
                ]

            # Se agrega cada producto a la tabla.
            for p in lista:

                # Se crea una fila usando los datos del producto.
                tabla.insert(
                    "",
                    "end",
                    iid=str(p["id"]),
                    values=(
                        p["id"],
                        p["nombre"],
                        p["categoria"],
                        p["franquicia"],
                        p["tipo"],
                        dinero(p["precio"]),
                        dinero(p["costo"]),
                        p["inventario"],
                        p["vendidos"]
                    )
                )

        # Cuando cambia el filtro, se vuelve a llenar la tabla.
        filtro.bind(
            "<<ComboboxSelected>>",
            lambda evento: llenar()
        )

        # Se llena la tabla por primera vez.
        llenar()

        # Se crea el espacio para los botones de la tabla.
        botones = tk.Frame(
            self.contenido,
            bg="#fff4e6"
        )
        botones.pack(
            fill="x",
            pady=8
        )

        # Obtiene el producto que está seleccionado en la tabla.
        def seleccionado():

            # Se obtiene la fila seleccionada.
            seleccion = tabla.selection()

            # Si no hay ninguna fila, se muestra un mensaje.
            if not seleccion:
                self.mensaje(
                    "Selecciona un producto de la tabla."
                )

                # Se devuelve None para indicar que no hay producto.
                return None

            # El ID de la fila se convierte en entero y se busca el producto.
            return buscar_producto(
                int(seleccion[0])
            )

        # Modifica el producto seleccionado.
        def modificar():

            # Se obtiene el producto.
            producto = seleccionado()

            # Si existe, se abre el formulario de modificación.
            if producto:
                self.formulario_producto(producto)

        # Elimina el producto seleccionado.
        def eliminar():

            # Se obtiene el producto seleccionado.
            producto = seleccionado()

            # Solo se continúa si existe un producto.
            if producto:

                # Se marca como inactivo.
                producto["activo"] = False

                # Se guardan los cambios.
                guardar_datos()

                # Se actualiza nuevamente el inventario.
                self.inventario()

                # Se informa el resultado.
                self.mensaje(
                    "Producto eliminado del inventario."
                )

        # Ajusta el stock del producto seleccionado.
        def ajustar():

            # Se obtiene el producto.
            producto = seleccionado()

            # Si existe, se abre la pantalla de ajuste.
            if producto:
                self.ajuste_producto(producto)

        # Botón para modificar.
        self.boton(
            botones,
            "Modificar",
            modificar
        ).pack(
            side="left",
            padx=3
        )

        # Botón para eliminar.
        self.boton(
            botones,
            "Eliminar",
            eliminar,
            "#c0392b"
        ).pack(
            side="left",
            padx=3
        )

        # Botón para ajustar stock.
        self.boton(
            botones,
            "Ajustar stock",
            ajustar,
            "#2874a6"
        ).pack(
            side="left",
            padx=3
        )

        # Se actualiza la información inferior.
        self.actualizar_estado()

    # -------------------- EXISTENCIAS --------------------

    # Permite aumentar o disminuir las existencias de un producto.
    def ajuste_producto(self, producto):

        # Se limpia la pantalla anterior.
        self.limpiar()

        # Se coloca el título.
        self.titulo("Ajustar existencias")

        # Se muestra el nombre y el stock actual.
        tk.Label(
            self.contenido,
            text=(
                f"{producto['nombre']}\n"
                f"Existencias actuales: {producto['inventario']}"
            ),
            bg="#fff4e6",
            fg="#7a4300",
            font=("Arial", 12, "bold")
        ).pack(
            anchor="w",
            pady=10
        )

        # Se explica cómo introducir el cambio.
        tk.Label(
            self.contenido,
            text=(
                "Escribe la cantidad que quieres agregar o retirar.\n"
                "Usa - para retirar."
            ),
            bg="#fff4e6",
            fg="#7a4300"
        ).pack(anchor="w")

        # Se crea la caja para escribir la cantidad.
        entrada = ttk.Entry(
            self.contenido,
            width=20
        )
        entrada.pack(
            anchor="w",
            pady=8
        )

        # Esta función aplica el cambio escrito.
        def aplicar():

            # Se intenta convertir el texto en un número entero.
            try:
                cambio = int(
                    entrada.get()
                )

                # No se permite un cambio de cero.
                if cambio == 0:
                    raise ValueError

                # Tampoco se permite que el inventario quede negativo.
                if producto["inventario"] + cambio < 0:
                    raise ValueError

            # Si el dato no cumple las condiciones, se muestra un mensaje.
            except ValueError:
                self.mensaje(
                    "Escribe un número válido y no retires más del stock."
                )
                return

            # Se suma el cambio al inventario actual.
            producto["inventario"] += cambio

            # Se guarda el nuevo inventario.
            guardar_datos()

            # Se regresa a la tabla.
            self.inventario()

            # Se informa que el cambio terminó.
            self.mensaje(
                "Existencias actualizadas."
            )

        # Botón para aplicar el cambio.
        self.boton(
            self.contenido,
            "Aplicar",
            aplicar
        ).pack(
            anchor="w",
            pady=5
        )

        # Botón para cancelar y volver al inventario.
        self.boton(
            self.contenido,
            "Cancelar",
            self.inventario,
            "#7f8c8d"
        ).pack(anchor="w")

    # Permite elegir un producto antes de ajustar sus existencias.
    def ajustar_existencias(self):

        # Primero se muestra la lista de productos activos.
        self.seleccionar_en_pantalla(
            "Ajustar existencias",
            self.ajuste_producto
        )

    # -------------------- VENTAS --------------------

    # Esta función muestra el formulario para registrar una venta.
    def registrar_venta(self):

        # Se obtiene la lista de productos que todavía están activos.
        lista = productos_activos()

        # Si no existen productos, no se puede registrar una venta.
        if not lista:
            self.mensaje(
                "No hay productos disponibles para vender."
            )
            return

        # Se limpia la pantalla anterior.
        self.limpiar()

        # Se coloca el título.
        self.titulo("Registrar venta")

        # Se crea el espacio del formulario.
        formulario = tk.Frame(
            self.contenido,
            bg="white",
            padx=20,
            pady=15
        )
        formulario.pack(
            fill="x",
            anchor="n"
        )

        # Se coloca la etiqueta Producto.
        tk.Label(
            formulario,
            text="Producto",
            bg="white",
            fg="#7a4300"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=8
        )

        # Se prepara el texto de cada producto para la lista.
        opciones = [
            f"ID {p['id']} - {p['nombre']} | Stock: {p['inventario']}"
            for p in lista
        ]

        # Se crea la lista desplegable de productos.
        combo = ttk.Combobox(
            formulario,
            values=opciones,
            state="readonly",
            width=55
        )

        # Se coloca la lista.
        combo.grid(
            row=0,
            column=1,
            sticky="w",
            pady=8
        )

        # Se selecciona el primer producto automáticamente.
        combo.current(0)

        # Se crea la etiqueta de cantidad.
        tk.Label(
            formulario,
            text="Cantidad",
            bg="white",
            fg="#7a4300"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=8
        )

        # Se crea la caja para escribir cuántas unidades se venden.
        cantidad = ttk.Entry(
            formulario,
            width=20
        )

        # Se coloca 1 como cantidad inicial.
        cantidad.insert(0, "1")

        # Se coloca la caja en el formulario.
        cantidad.grid(
            row=1,
            column=1,
            sticky="w",
            pady=8
        )

        # Se crea la etiqueta para el descuento.
        tk.Label(
            formulario,
            text="Descuento (%)",
            bg="white",
            fg="#7a4300"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=8
        )

        # Se crea la caja para el descuento.
        descuento = ttk.Entry(
            formulario,
            width=20
        )

        # El descuento comienza en cero.
        descuento.insert(0, "0")

        # Se coloca la caja en el formulario.
        descuento.grid(
            row=2,
            column=1,
            sticky="w",
            pady=8
        )

        # Esta función realiza y guarda la venta.
        def vender():

            # Se obtiene el producto seleccionado.
            producto = lista[combo.current()]

            # Se intenta convertir cantidad y descuento a números.
            try:

                # La cantidad debe ser un entero.
                unidades = int(
                    cantidad.get()
                )

                # El descuento puede tener decimales.
                porcentaje = float(
                    descuento.get().replace(",", ".")
                )

                # Se validan los límites permitidos.
                if (
                    unidades <= 0
                    or porcentaje < 0
                    or porcentaje > 100
                ):
                    raise ValueError

            # Si algo no es válido, se muestra un mensaje.
            except ValueError:
                self.mensaje(
                    "Cantidad o descuento incorrectos."
                )
                return

            # Se revisa que haya suficiente stock.
            if unidades > producto["inventario"]:
                self.mensaje(
                    "No hay suficientes unidades en inventario."
                )
                return

            # Se calcula el precio después del descuento.
            precio_final = producto["precio"] * (
                1 - porcentaje / 100
            )

            # Se calcula cuánto dinero entró por la venta.
            ingreso = precio_final * unidades

            # Se calcula la ganancia restando el costo.
            ganancia = (
                precio_final - producto["costo"]
            ) * unidades

            # Se descuentan las unidades vendidas del inventario.
            producto["inventario"] -= unidades

            # Se suman las unidades a las ventas del producto.
            producto["vendidos"] += unidades

            # Se acumula el ingreso obtenido.
            producto["ingresos"] += ingreso

            # Se acumula la ganancia obtenida.
            producto["ganancia"] += ganancia

            # Se crea un registro con los datos de la venta.
            ventas.append({
                "fecha": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "id_producto": producto["id"],
                "producto": producto["nombre"],
                "cantidad": unidades,
                "precio_unitario": precio_final,
                "descuento": porcentaje,
                "ingreso": ingreso,
                "ganancia": ganancia
            })

            # Se guardan todos los cambios.
            guardar_datos()

            # Se regresa al inventario para ver el nuevo stock.
            self.inventario()

            # Se muestra el mensaje de venta registrada.
            self.mensaje(
                "Venta registrada correctamente."
            )

        # Botón que ejecuta la venta.
        self.boton(
            self.contenido,
            "Registrar venta",
            vender,
            "#2874a6"
        ).pack(
            anchor="w",
            pady=12
        )

    # -------------------- REPORTES SENCILLOS --------------------

    # Muestra las unidades vendidas y el nivel de demanda de cada producto.
    def analisis_demanda(self):

        # Se limpia la pantalla.
        self.limpiar()

        # Se coloca el título.
        self.titulo("Análisis de demanda")

        # Se obtiene la lista de productos activos.
        lista = productos_activos()

        # Si no hay productos, se muestra un mensaje.
        if not lista:
            tk.Label(
                self.contenido,
                text="No hay productos para analizar.",
                bg="#fff4e6",
                fg="#7a4300"
            ).pack(anchor="w")
            return

        # Se muestra cada producto y sus ventas.
        for p in lista:

            # Se crea el texto que resume la información.
            texto = (
                f"{p['nombre']} | "
                f"Vendidos: {p['vendidos']} | "
                f"Demanda: {demanda(p)}"
            )

            # Se coloca el resultado en la pantalla.
            tk.Label(
                self.contenido,
                text=texto,
                bg="white",
                fg="#7a4300",
                anchor="w",
                padx=10,
                pady=9
            ).pack(
                fill="x",
                pady=2
            )

    # Muestra un resumen general de productos, ventas, ingresos y ganancias.
    def resumen_general(self):

        # Se limpia la pantalla.
        self.limpiar()

        # Se coloca el título.
        self.titulo("Resumen general")

        # Se obtiene la lista de productos activos.
        lista = productos_activos()

        # Si existen productos, se busca el que más unidades haya vendido.
        if lista:
            mas_vendido = max(
                lista,
                key=lambda p: p["vendidos"]
            )

            # Se guarda su nombre para mostrarlo después.
            nombre_mas_vendido = mas_vendido["nombre"]

        # Si no hay productos, se muestra un texto sencillo.
        else:
            nombre_mas_vendido = "No hay productos"

        # Se preparan los datos que se mostrarán.
        datos = [
            ("Productos activos", len(lista)),
            (
                "Unidades vendidas",
                sum(p["vendidos"] for p in lista)
            ),
            (
                "Ingresos totales",
                dinero(sum(p["ingresos"] for p in lista))
            ),
            (
                "Ganancias totales",
                dinero(sum(p["ganancia"] for p in lista))
            ),
            (
                "Producto más vendido",
                nombre_mas_vendido
            )
        ]

        # Se recorre cada dato para mostrarlo en una línea.
        for nombre, valor in datos:

            # Se crea una etiqueta con el nombre y el valor.
            tk.Label(
                self.contenido,
                text=f"{nombre}: {valor}",
                bg="white",
                fg="#7a4300",
                font=("Arial", 11, "bold"),
                anchor="w",
                padx=12,
                pady=10
            ).pack(
                fill="x",
                pady=2
            )

    # Muestra una tabla con todas las ventas registradas.
    def historial_ventas(self):

        # Se limpia la pantalla anterior.
        self.limpiar()

        # Se coloca el título.
        self.titulo("Historial de ventas")

        # Se definen las columnas de la tabla.
        columnas = (
            "fecha",
            "id",
            "producto",
            "cantidad",
            "precio",
            "descuento",
            "ingreso"
        )

        # Se crea la tabla.
        tabla = ttk.Treeview(
            self.contenido,
            columns=columnas,
            show="headings"
        )

        # Estos son los nombres visibles de las columnas.
        nombres = [
            "Fecha",
            "ID",
            "Producto",
            "Cantidad",
            "Precio",
            "Descuento",
            "Ingreso"
        ]

        # Se configura cada columna.
        for columna, nombre in zip(columnas, nombres):

            # Se coloca el nombre de la columna.
            tabla.heading(
                columna,
                text=nombre
            )

            # Se define su tamaño y alineación.
            tabla.column(
                columna,
                width=110,
                anchor="center"
            )

        # reversed hace que primero aparezcan las ventas más recientes.
        for venta in reversed(ventas):

            # Se agrega una venta como una nueva fila.
            tabla.insert(
                "",
                "end",
                values=(
                    venta.get("fecha", ""),
                    venta.get("id_producto", ""),
                    venta.get("producto", ""),
                    venta.get("cantidad", 0),
                    dinero(
                        venta.get(
                            "precio_unitario",
                            0
                        )
                    ),
                    f"{venta.get('descuento', 0)}%",
                    dinero(
                        venta.get(
                            "ingreso",
                            0
                        )
                    )
                )
            )

        # Se muestra la tabla en la pantalla.
        tabla.pack(
            fill="both",
            expand=True
        )


# -------------------- ARRANQUE DEL PROGRAMA --------------------

# Primero se cargan los productos y las ventas guardadas.
cargar_datos()

# iniciar_sesion crea la primera pantalla.
# Si el usuario escribe admin y 1234, entonces abre el inventario.
def abrir_programa():

    # Se crea una nueva ventana de Tkinter.
    ventana = tk.Tk()

    # Se crea el programa principal dentro de esa ventana.
    programa = Programa(ventana)

    # mainloop mantiene funcionando la ventana principal.
    ventana.mainloop()


# Se inicia primero la pantalla de inicio de sesión.
iniciar_sesion()
