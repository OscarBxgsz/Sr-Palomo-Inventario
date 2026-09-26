# SISTEMA DE INVENTARIO - SR. PALOMO
#Creacion del codigo: 20/08/2026. Hecha por Julio.
#Modificacion numero 1 (Empezar con la organización del código, crear la base del sistema): 28 y 29 de agosto de 2026. Hecha por Ronn.
#Modificacion numero 2 (Agregar funcionalidad para registrar ventas): 31 de agosto y 1 de septiembre de 2026. Hecha por Ronn.
#Modificacion numero 3 (Agregar funcionalidad para registrar productos): 17/09/2026. Hecha por Julio.
#Modificacion numero 4 (Debugging, arreglar errores del código): 22/09/2026. Hecha por Ronn.
#Modificación número 5 (Mejoras en la interfaz de usuario y muchas más funciones añadidas): 24/09/2026. Hecha por Oscar.

# Se importan las herramientas necesarias para crear la interfaz gráfica.
import tkinter as tk
# ttk agrega controles gráficos como cajas de texto y tablas, y messagebox muestra avisos.
from tkinter import ttk, messagebox
# json permite guardar y recuperar los datos, mientras os ayuda a construir rutas de archivos.
import json, os
# datetime permite registrar la fecha y hora de cada venta.
from datetime import datetime

# Se obtiene la carpeta donde está este archivo para guardar el JSON siempre en el mismo lugar.
CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(CARPETA, "productos_sr_palomo.json")

productos = []
ventas = []
siguiente_id = 1

ventana_principal = None
contenido = None


# -------------------- DATOS --------------------

def guardar_datos():
    # Esta función guarda productos, ventas y el siguiente ID en el archivo JSON.
    datos = {}
    datos["productos"] = productos
    datos["ventas"] = ventas
    datos["siguiente_id"] = siguiente_id

    # Se intenta abrir el archivo para escribir los datos actuales.
    try:
        archivo = open(ARCHIVO, "w", encoding="utf-8")
        json.dump(datos, archivo, indent=4)
        archivo.close()

    # Si Windows no permite escribir, se muestra un aviso en lugar de cerrar el programa.
    except PermissionError:
        messagebox.showerror(
            "Error al guardar",
            "No se puede guardar el archivo productos_sr_palomo.json. "
            "Cierra el archivo JSON si está abierto y vuelve a intentarlo."
        )


# Esta función carga del archivo JSON los datos guardados anteriormente.
def cargar_datos():
    global productos, ventas, siguiente_id

    try:
        archivo = open(ARCHIVO, "r", encoding="utf-8")
        datos = json.load(archivo)
        archivo.close()

        if "productos" in datos:
            productos = datos["productos"]

        if "ventas" in datos:
            ventas = datos["ventas"]

        if "siguiente_id" in datos:
            siguiente_id = datos["siguiente_id"]

        for p in productos:
            if "activo" not in p:
                p["activo"] = True
            if "vendidos" not in p:
                p["vendidos"] = 0
            if "ingresos" not in p:
                p["ingresos"] = 0
            if "ganancia" not in p:
                p["ganancia"] = 0

    except FileNotFoundError:
        productos = []
        ventas = []
        siguiente_id = 1

    except json.JSONDecodeError:
        productos = []
        ventas = []
        siguiente_id = 1


# Busca un producto en la lista usando su ID.
def buscar_producto(identificador):
    for p in productos:
        if p["id"] == identificador:
            return p

    return None


# Devuelve una lista con los productos que siguen activos.
def productos_activos():
    activos = []

    for p in productos:
        if p["activo"] == True:
            activos.append(p)

    return activos


# Suma un dato específico de todos los productos de una lista.
def total(lista, dato):
    suma = 0

    for p in lista:
        suma = suma + p[dato]

    return suma


# Convierte un número a un texto con formato de dinero.
def dinero(cantidad):
    return f"${cantidad:.2f}"


# Clasifica la demanda según las unidades vendidas.
def demanda(p):
    if p["vendidos"] >= 100:
        return "Alta"
    elif p["vendidos"] >= 50:
        return "Media"
    else:
        return "Baja"


# -------------------- INTERFAZ GENERAL --------------------

# Borra los elementos que aparecen actualmente en el área de contenido.
def limpiar():
    for widget in contenido.winfo_children():
        widget.destroy()


# Muestra el título de la sección que está abierta.
def titulo(texto):
    tk.Label(
        contenido,
        text=texto,
        font=("Arial", 18, "bold")
    ).pack(anchor="w", pady=10)


# Crea un botón sencillo y lo conecta con una función.
def boton(padre, texto, funcion):
    tk.Button(
        padre,
        text=texto,
        command=funcion
    ).pack(anchor="w", pady=3)


# -------------------- LOGIN --------------------

# Crea la ventana de inicio de sesión y comprueba las credenciales.
def iniciar_sesion():
    ventana = tk.Tk()
    ventana.title("Sr. Palomo - Inicio de sesión")
    ventana.geometry("380x280")

    tk.Label(
        ventana,
        text="SR. PALOMO",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(ventana, text="Usuario").pack()

    usuario = tk.Entry(ventana)
    usuario.pack()

    tk.Label(ventana, text="Contraseña").pack(pady=5)

    contrasena = tk.Entry(ventana, show="*")
    contrasena.pack()

    def comprobar(event=None):
        if usuario.get() == "admin" and contrasena.get() == "1234":
            ventana.destroy()
            abrir_programa()
        else:
            messagebox.showerror(
                "Acceso",
                "Usuario o contraseña incorrectos."
            )

    tk.Button(
        ventana,
        text="Iniciar sesión",
        command=comprobar
    ).pack(pady=15)

    ventana.bind("<Return>", comprobar)
    usuario.focus()
    ventana.mainloop()


# -------------------- INICIO Y RESUMEN --------------------

# Muestra en una sola pantalla el inicio y el resumen general del sistema.
def inicio():
    limpiar()
    titulo("Bienvenido a Sr. Palomo")

    lista = productos_activos()

    tk.Label(
        contenido,
        text="Productos activos: " + str(len(lista))
    ).pack(anchor="w")

    unidades = total(lista, "vendidos")
    tk.Label(
        contenido,
        text="Unidades vendidas: " + str(unidades)
    ).pack(anchor="w")

    ingresos = total(lista, "ingresos")
    tk.Label(
        contenido,
        text="Ingresos totales: " + dinero(ingresos)
    ).pack(anchor="w")

    ganancias = total(lista, "ganancia")
    tk.Label(
        contenido,
        text="Ganancias totales: " + dinero(ganancias)
    ).pack(anchor="w")

    mas_vendido = "No hay productos"

    if len(lista) > 0:
        mas_vendido = lista[0]["nombre"]
        mayor = lista[0]["vendidos"]

        for p in lista:
            if p["vendidos"] > mayor:
                mayor = p["vendidos"]
                mas_vendido = p["nombre"]

    tk.Label(
        contenido,
        text="Producto más vendido: " + mas_vendido
    ).pack(anchor="w")


# -------------------- PRODUCTOS --------------------

# Crea el formulario para registrar o modificar un producto.
def formulario_producto(producto=None):
    global siguiente_id

    limpiar()

    # Se determina si el formulario se usará para modificar o registrar.
    editar = False

    if producto != None:
        editar = True
        titulo("Modificar producto")
    else:
        titulo("Registrar producto")

    tk.Label(contenido, text="Nombre").pack(anchor="w")
    entrada_nombre = tk.Entry(contenido, width=40)
    entrada_nombre.pack(anchor="w")

    tk.Label(contenido, text="Franquicia / Anime o serie").pack(anchor="w")
    entrada_franquicia = tk.Entry(contenido, width=40)
    entrada_franquicia.pack(anchor="w")

    tk.Label(contenido, text="Tipo de producto").pack(anchor="w")
    entrada_tipo = tk.Entry(contenido, width=40)
    entrada_tipo.pack(anchor="w")

    tk.Label(contenido, text="Precio de venta").pack(anchor="w")
    entrada_precio = tk.Entry(contenido, width=40)
    entrada_precio.pack(anchor="w")

    tk.Label(contenido, text="Costo de producción").pack(anchor="w")
    entrada_costo = tk.Entry(contenido, width=40)
    entrada_costo.pack(anchor="w")

    tk.Label(contenido, text="Cantidad en inventario").pack(anchor="w")
    entrada_inventario = tk.Entry(contenido, width=40)
    entrada_inventario.pack(anchor="w")

    if editar:
        entrada_nombre.insert(0, producto["nombre"])
        entrada_franquicia.insert(0, producto["franquicia"])
        entrada_tipo.insert(0, producto["tipo"])
        entrada_precio.insert(0, str(producto["precio"]))
        entrada_costo.insert(0, str(producto["costo"]))
        entrada_inventario.insert(0, str(producto["inventario"]))

    # Esta función valida y guarda la información que el usuario escribió.
    def guardar():
        global siguiente_id

        nombre = entrada_nombre.get()
        franquicia = entrada_franquicia.get()
        tipo = entrada_tipo.get()

        if nombre == "" or franquicia == "" or tipo == "":
            messagebox.showwarning(
                "Datos",
                "Completa los campos de texto."
            )
            return

        try:
            precio = float(entrada_precio.get())
            costo = float(entrada_costo.get())
            inventario_nuevo = int(entrada_inventario.get())

            if precio < 0 or costo < 0 or inventario_nuevo < 0:
                raise ValueError

            if precio < costo:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Datos",
                "Precio, costo e inventario deben ser válidos."
            )
            return

        if editar:
            producto["nombre"] = nombre
            producto["franquicia"] = franquicia
            producto["tipo"] = tipo
            producto["precio"] = precio
            producto["costo"] = costo
            producto["inventario"] = inventario_nuevo

        else:
            nuevo = {}
            nuevo["id"] = siguiente_id
            nuevo["nombre"] = nombre
            nuevo["franquicia"] = franquicia
            nuevo["tipo"] = tipo
            nuevo["precio"] = precio
            nuevo["costo"] = costo
            nuevo["inventario"] = inventario_nuevo
            nuevo["vendidos"] = 0
            nuevo["ingresos"] = 0
            nuevo["ganancia"] = 0
            nuevo["activo"] = True

            productos.append(nuevo)
            siguiente_id = siguiente_id + 1

        guardar_datos()
        inventario()
        messagebox.showinfo("Inventario", "Producto guardado correctamente.")

    boton(contenido, "Guardar", guardar)
    boton(contenido, "Cancelar", inventario)


# Abre el formulario para registrar un producto nuevo.
def registrar_producto():
    formulario_producto()


# -------------------- SELECCIONAR PRODUCTO --------------------

# Permite seleccionar un producto antes de modificarlo, eliminarlo o ajustarlo.
def seleccionar_producto(titulo_texto, funcion):
    limpiar()
    titulo(titulo_texto)

    lista = productos_activos()

    if len(lista) == 0:
        tk.Label(
            contenido,
            text="No hay productos registrados."
        ).pack(anchor="w")
        return

    tk.Label(
        contenido,
        text="Selecciona un producto:"
    ).pack(anchor="w")

    lista_texto = []

    for p in lista:
        texto = "ID " + str(p["id"]) + " - " + p["nombre"]
        lista_texto.append(texto)

    combo = ttk.Combobox(
        contenido,
        values=lista_texto,
        state="readonly"
    )
    combo.pack(anchor="w", pady=5)
    combo.current(0)

    # Continúa con el producto que el usuario seleccionó.
    def continuar():
        numero = combo.current()
        funcion(lista[numero])

    boton(contenido, "Continuar", continuar)


# Selecciona un producto y abre su formulario de modificación.
def modificar_producto():
    seleccionar_producto(
        "Modificar producto",
        formulario_producto
    )


# Selecciona un producto y lo marca como inactivo.
def eliminar_producto():
    def eliminar(producto):
        producto["activo"] = False
        guardar_datos()
        inventario()
        messagebox.showinfo("Inventario", "Producto eliminado del inventario.")

    seleccionar_producto(
        "Eliminar producto",
        eliminar
    )


# -------------------- INVENTARIO --------------------

# Muestra los productos activos y las acciones disponibles sobre el inventario.
def inventario():
    limpiar()
    titulo("Inventario")

    lista = productos_activos()

    if len(lista) == 0:
        tk.Label(
            contenido,
            text="No hay productos registrados."
        ).pack(anchor="w")
    else:
        for p in lista:
            texto = (
                "ID: " + str(p["id"]) +
                " | " + p["nombre"] +
                " | Stock: " + str(p["inventario"]) +
                " | Vendidos: " + str(p["vendidos"])
            )

            tk.Label(
                contenido,
                text=texto
            ).pack(anchor="w", pady=2)

    boton(contenido, "Modificar producto", modificar_producto)
    boton(contenido, "Eliminar producto", eliminar_producto)
    boton(contenido, "Ajustar stock", ajustar_existencias)


# -------------------- EXISTENCIAS --------------------

# Permite aumentar o disminuir las existencias de un producto.
def ajuste_producto(producto):
    limpiar()
    titulo("Ajustar existencias")

    tk.Label(
        contenido,
        text="Producto: " + producto["nombre"]
    ).pack(anchor="w")

    tk.Label(
        contenido,
        text="Stock actual: " + str(producto["inventario"])
    ).pack(anchor="w")

    tk.Label(
        contenido,
        text="Escribe una cantidad. Usa - para retirar."
    ).pack(anchor="w", pady=5)

    entrada = tk.Entry(contenido)
    entrada.pack(anchor="w")

    def aplicar():
        try:
            cambio = int(entrada.get())

            if cambio == 0:
                raise ValueError

            if producto["inventario"] + cambio < 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Stock",
                "Escribe un número válido."
            )
            return

        producto["inventario"] = producto["inventario"] + cambio
        guardar_datos()
        inventario()

    boton(contenido, "Aplicar", aplicar)
    boton(contenido, "Cancelar", inventario)


# Permite seleccionar el producto al que se le ajustará el stock.
def ajustar_existencias():
    seleccionar_producto(
        "Ajustar existencias",
        ajuste_producto
    )


# -------------------- VENTAS --------------------

# Registra una venta, actualiza el inventario y guarda sus resultados.
def registrar_venta():
    limpiar()
    titulo("Registrar venta")

    lista = productos_activos()

    if len(lista) == 0:
        messagebox.showwarning(
            "Venta",
            "No hay productos disponibles."
        )
        return

    tk.Label(contenido, text="ID del producto").pack(anchor="w")
    entrada_id = tk.Entry(contenido)
    entrada_id.pack(anchor="w")
    entrada_id.insert(0, str(lista[0]["id"]))

    tk.Label(contenido, text="Cantidad").pack(anchor="w")
    entrada_cantidad = tk.Entry(contenido)
    entrada_cantidad.pack(anchor="w")
    entrada_cantidad.insert(0, "1")

    tk.Label(contenido, text="Descuento (%)").pack(anchor="w")
    entrada_descuento = tk.Entry(contenido)
    entrada_descuento.pack(anchor="w")
    entrada_descuento.insert(0, "0")

    # Esta función valida la venta, hace los cálculos y actualiza los datos.
    def vender():
        try:
            identificador = int(entrada_id.get())
            cantidad = int(entrada_cantidad.get())
            descuento = float(entrada_descuento.get())

            producto = buscar_producto(identificador)

            if producto == None:
                raise ValueError

            if cantidad <= 0:
                raise ValueError

            if descuento < 0 or descuento > 100:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Venta",
                "Revisa el ID, cantidad y descuento."
            )
            return

        if cantidad > producto["inventario"]:
            messagebox.showwarning(
                "Venta",
                "No hay suficientes unidades."
            )
            return

        precio_final = producto["precio"] * (1 - descuento / 100)
        ingreso = precio_final * cantidad
        ganancia = (precio_final - producto["costo"]) * cantidad

        producto["inventario"] = producto["inventario"] - cantidad
        producto["vendidos"] = producto["vendidos"] + cantidad
        producto["ingresos"] = producto["ingresos"] + ingreso
        producto["ganancia"] = producto["ganancia"] + ganancia

        venta = {}
        venta["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        venta["id_producto"] = producto["id"]
        venta["producto"] = producto["nombre"]
        venta["cantidad"] = cantidad
        venta["precio_unitario"] = precio_final
        venta["descuento"] = descuento
        venta["ingreso"] = ingreso
        venta["ganancia"] = ganancia

        ventas.append(venta)

        guardar_datos()
        inventario()

        messagebox.showinfo(
            "Venta",
            "Venta registrada correctamente."
        )

    boton(contenido, "Registrar venta", vender)


# -------------------- DEMANDA --------------------

# Muestra las unidades vendidas y la demanda de cada producto.
def analisis_demanda():
    limpiar()
    titulo("Análisis de demanda")

    lista = productos_activos()

    if len(lista) == 0:
        tk.Label(
            contenido,
            text="No hay productos para analizar."
        ).pack(anchor="w")
        return

    for p in lista:
        texto = (
            p["nombre"] +
            " | Vendidos: " +
            str(p["vendidos"]) +
            " | Demanda: " +
            demanda(p)
        )

        tk.Label(
            contenido,
            text=texto
        ).pack(anchor="w", pady=2)


# -------------------- HISTORIAL --------------------

# Muestra las ventas registradas empezando por la más reciente.
def historial_ventas():
    limpiar()
    titulo("Historial de ventas")

    if len(ventas) == 0:
        tk.Label(
            contenido,
            text="No hay ventas registradas."
        ).pack(anchor="w")
        return

    numero = len(ventas) - 1

    while numero >= 0:
        v = ventas[numero]

        texto = (
            v["fecha"] +
            " | Producto: " + v["producto"] +
            " | Cantidad: " + str(v["cantidad"]) +
            " | Precio: " + dinero(v["precio_unitario"]) +
            " | Descuento: " + str(v["descuento"]) + "%" +
            " | Ingreso: " + dinero(v["ingreso"])
        )

        tk.Label(
            contenido,
            text=texto
        ).pack(anchor="w", pady=2)

        numero = numero - 1


# -------------------- PROGRAMA PRINCIPAL --------------------

# Crea la ventana principal y mantiene activa la interfaz.
def abrir_programa():
    global ventana_principal
    global contenido

    ventana_principal = tk.Tk()
    ventana_principal.title("Sr. Palomo - Inventario")
    ventana_principal.geometry("850x550")

    menu = tk.Frame(ventana_principal)
    menu.pack(fill="x")

    tk.Button(menu, text="Inicio", command=inicio).pack(side="left")
    tk.Button(menu, text="Productos", command=registrar_producto).pack(side="left")
    tk.Button(menu, text="Inventario", command=inventario).pack(side="left")
    tk.Button(menu, text="Venta", command=registrar_venta).pack(side="left")
    tk.Button(menu, text="Demanda", command=analisis_demanda).pack(side="left")
    tk.Button(menu, text="Historial", command=historial_ventas).pack(side="left")

    contenido = tk.Frame(ventana_principal)
    contenido.pack(fill="both", expand=True, padx=15, pady=15)

    inicio()
    ventana_principal.mainloop()


cargar_datos()
iniciar_sesion()
