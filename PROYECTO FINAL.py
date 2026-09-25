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

# Se obtiene la carpeta donde se encuentra este archivo Python.
CARPETA = os.path.dirname(os.path.abspath(__file__))
# Se construye la ruta del archivo JSON donde se guardan los datos.
ARCHIVO = os.path.join(CARPETA, 'productos_sr_palomo.json')
# Se crean las listas que almacenarán productos y ventas.
productos, ventas = [], []
# Se define el primer ID disponible para un producto nuevo.
siguiente_id = 1

# Guarda en el archivo JSON toda la información actual del programa.
def guardar_datos():
    # Se abre el archivo en modo escritura para reemplazar su contenido con los datos actuales.
    with open(ARCHIVO, 'w', encoding='utf-8') as archivo:
        # Se convierten productos, ventas y siguiente_id a formato JSON y se escriben en el archivo.
        json.dump({'productos': productos, 'ventas': ventas, 'siguiente_id': siguiente_id}, archivo, ensure_ascii=False, indent=4)

# Carga desde el archivo JSON la información guardada anteriormente.
def cargar_datos():
    # Se indica que estas variables globales serán actualizadas dentro de la función.
    global productos, ventas, siguiente_id
    # Se intenta abrir y leer el archivo existente.
    try:
        # Se abre el archivo en modo lectura.
        with open(ARCHIVO, 'r', encoding='utf-8') as archivo:
            # Se convierten los datos JSON en estructuras de Python.
            datos = json.load(archivo)
        # Se recupera la lista de productos o una lista vacía si no existe.
        productos = datos.get('productos', [])
        # Se recupera la lista de ventas o una lista vacía si no existe.
        ventas = datos.get('ventas', [])
        # Se recupera el siguiente ID o se usa 1 si todavía no existe.
        siguiente_id = datos.get('siguiente_id', 1)
        # Se revisan los productos para completar datos que pudieran no existir en archivos anteriores.
        for p in productos:
            # Se establece el estado activo y el número de unidades vendidas inicial.
            p.setdefault('activo', True); p.setdefault('vendidos', 0)
            # Se establecen ingresos y ganancias iniciales cuando faltan.
            p.setdefault('ingresos', 0); p.setdefault('ganancia', 0)
    # Si el archivo no existe o contiene JSON inválido, se inicia el programa con datos vacíos.
    except (FileNotFoundError, json.JSONDecodeError):
        # Se reinician las listas y el siguiente ID.
        productos, ventas, siguiente_id = [], [], 1

# Busca un producto por su número de identificación.
def buscar_producto(identificador):
    # Se recorre la lista y se devuelve el primer producto cuyo ID coincida; si no hay coincidencia, se devuelve None.
    return next((p for p in productos if p['id'] == identificador), None)

# Devuelve solamente los productos que siguen activos en el inventario.
def productos_activos():
    # Se filtran los productos cuyo campo activo sea True o que no tengan ese campo.
    return [p for p in productos if p.get('activo', True)]

# Suma los valores de un mismo dato en todos los productos de una lista.
def total(lista, dato):
    # Se recorren los productos y se suman los valores del campo indicado.
    return sum(p.get(dato, 0) for p in lista)

# Convierte un número en un texto con formato de dinero y dos decimales.
def dinero(cantidad):
    # Se devuelve la cantidad con signo de peso y dos cifras decimales.
    return f'${cantidad:.2f}'

# Clasifica la demanda de un producto usando sus unidades vendidas.
def demanda(p):
    # Con 100 o más unidades vendidas la demanda es Alta; con 50 o más es Media; en otro caso es Baja.
    return 'Alta' if p['vendidos'] >= 100 else 'Media' if p['vendidos'] >= 50 else 'Baja'

# Crea la ventana donde el usuario introduce sus credenciales.
def iniciar_sesion():
    # Se crea la ventana principal del inicio de sesión.
    ventana = tk.Tk()
    # Se coloca el título de la ventana.
    ventana.title('Sr. Palomo - Inicio de sesión')
    # Se define el tamaño de la ventana y se evita modificarlo.
    ventana.geometry('400x300'); ventana.resizable(False, False); ventana.configure(bg='#fff4e6')
    # Se muestra el nombre del sistema en la parte superior.
    tk.Label(ventana, text='SR. PALOMO', bg='#fff4e6', fg='#7a4300', font=('Arial', 20, 'bold')).pack(pady=(30, 8))
    # Se muestra una indicación para entrar al sistema.
    tk.Label(ventana, text='Inicia sesión para entrar al sistema', bg='#fff4e6', fg='#8a6a4a').pack(pady=5)
    # Se coloca la etiqueta del campo de usuario.
    tk.Label(ventana, text='Usuario', bg='#fff4e6', fg='#7a4300').pack()
    # Se crea la caja donde el usuario escribirá su nombre.
    usuario = ttk.Entry(ventana, width=30); usuario.pack(pady=5)
    # Se coloca la etiqueta del campo de contraseña.
    tk.Label(ventana, text='Contraseña', bg='#fff4e6', fg='#7a4300').pack()
    # Se crea la caja de contraseña ocultando los caracteres escritos.
    contrasena = ttk.Entry(ventana, width=30, show='*'); contrasena.pack(pady=5)
    # Comprueba las credenciales cuando el usuario intenta iniciar sesión.
    def comprobar(event=None):
        # Se valida que el usuario sea admin y la contraseña sea 1234.
        if usuario.get() == 'admin' and contrasena.get() == '1234':
            # Se cierra la ventana de acceso y se abre el programa principal.
            ventana.destroy(); abrir_programa()
        # Si las credenciales no coinciden, se muestra un aviso de error.
        else:
            messagebox.showerror('Acceso', 'Usuario o contraseña incorrectos.')
    # Se crea el botón que ejecuta la comprobación de las credenciales.
    tk.Button(ventana, text='Iniciar sesión', command=comprobar, bg='#ff9c1d', fg='white', padx=16, pady=6).pack(pady=8)
    # La tecla Enter ejecuta la comprobación, se enfoca el usuario y se inicia el bucle de la ventana.
    ventana.bind('<Return>', comprobar); usuario.focus(); ventana.mainloop()

# Agrupa la lógica de la ventana principal del sistema.
class Programa:
    # Inicializa la interfaz principal y sus componentes.
    def __init__(self, ventana):
        # Se guarda la ventana recibida para poder trabajar con ella desde los métodos.
        self.ventana = ventana
        # Se establece el título, tamaño y color de fondo de la ventana principal.
        ventana.title('Sr. Palomo - Inventario'); ventana.geometry('1000x620'); ventana.configure(bg='#fff4e6')
        # Se crea el encabezado superior de la aplicación.
        encabezado = tk.Frame(ventana, bg='#ff9c1d')
        # El encabezado ocupa todo el ancho disponible.
        encabezado.pack(fill='x')
        # Se muestra el nombre de Sr. Palomo en el encabezado.
        tk.Label(encabezado, text='SR. PALOMO', bg='#ff9c1d', fg='white', font=('Arial', 20, 'bold')).pack(side='left', padx=15, pady=10)
        # Se define el menú horizontal con las secciones que puede abrir el usuario.
        menu = [('Inicio', self.inicio), ('Productos', self.registrar_producto), ('Inventario', self.inventario),
                ('Venta', self.registrar_venta), ('Demanda', self.analisis_demanda), ('Historial', self.historial_ventas)]
        # Se crea un botón para cada opción del menú.
        for texto, funcion in menu:
            # El botón ejecuta la función asociada cuando el usuario hace clic.
            tk.Button(encabezado, text=texto, command=funcion, bg='#7a4300', fg='white', relief='flat', padx=7, pady=5).pack(side='left', padx=2, pady=10)
        # Se crea el espacio central donde se mostrará cada pantalla.
        self.contenido = tk.Frame(ventana, bg='#fff4e6')
        # El área central ocupa el espacio restante de la ventana.
        self.contenido.pack(fill='both', expand=True, padx=18, pady=18)
        # Al abrir la aplicación se muestra directamente la pantalla de inicio.
        self.inicio()

    # Elimina los widgets de la pantalla actual para poder cargar otra sección.
    def limpiar(self):
        # Se recorre cada widget que existe dentro del área de contenido.
        for widget in self.contenido.winfo_children(): widget.destroy()

    # Crea un título y opcionalmente una descripción para cada pantalla.
    def titulo(self, texto, descripcion=''):
        # Se muestra el título principal de la sección.
        tk.Label(self.contenido, text=texto, bg='#fff4e6', fg='#7a4300', font=('Arial', 18, 'bold')).pack(anchor='w', pady=(0, 5))
        # Solo se crea una segunda etiqueta cuando se recibe una descripción.
        if descripcion:
            # Se muestra la descripción debajo del título.
            tk.Label(self.contenido, text=descripcion, bg='#fff4e6', fg='#8a6a4a').pack(anchor='w', pady=(0, 10))

    # Crea botones reutilizables para las diferentes pantallas del programa.
    def boton(self, padre, texto, funcion, color='#ff9c1d'):
        # Devuelve un botón ya configurado con el texto, función y color indicados.
        return tk.Button(padre, text=texto, command=funcion, bg=color, fg='white', padx=10, pady=5)

    # Muestra la pantalla inicial con la información general del sistema.
    def inicio(self):
        # Se limpia la pantalla anterior y se coloca el título de inicio.
        self.limpiar(); self.titulo('Bienvenido a Sr. Palomo', 'Sistema de gestión de inventario')
        # Se obtienen solamente los productos activos para calcular los datos mostrados.
        lista = productos_activos()
        # Se localiza el producto con más unidades vendidas para incluirlo en el resumen del inicio.
        mas_vendido = max(lista, key=lambda p: p['vendidos'], default=None)
        # Se preparan los mismos datos que antes se mostraban en la pestaña de resumen.
        datos = [('Productos activos', len(lista)), ('Unidades vendidas', total(lista, 'vendidos')), ('Ingresos totales', dinero(total(lista, 'ingresos'))), ('Ganancias totales', dinero(total(lista, 'ganancia'))), ('Producto más vendido', mas_vendido['nombre'] if mas_vendido else 'No hay productos')]
        # Se recorren los datos para mostrarlos uno debajo de otro en la pantalla de inicio.
        for nombre, valor in datos:
            # Cada dato se presenta en una etiqueta con formato de resumen.
            tk.Label(self.contenido, text=f'{nombre}: {valor}', bg='white', fg='#7a4300', font=('Arial', 11, 'bold'), anchor='w', padx=12, pady=10).pack(fill='x', pady=2)

    # Crea el formulario para registrar un producto nuevo o modificar uno existente.
    def formulario_producto(self, producto=None):
        # Se permite actualizar el siguiente ID cuando se registre un producto nuevo.
        global siguiente_id
        # Se limpia la pantalla y se determina si el formulario está editando un producto.
        self.limpiar(); editar = producto is not None
        # Se cambia el título según se trate de registro o modificación.
        self.titulo('Modificar producto' if editar else 'Registrar producto')
        # Se crea el contenedor visual del formulario.
        formulario = tk.Frame(self.contenido, bg='white', padx=20, pady=15); formulario.pack(fill='x')
        # Se definen las etiquetas visibles y las claves usadas para almacenar cada dato.
        campos, etiquetas = {}, [('Nombre', 'nombre'), ('Franquicia / Anime o serie', 'franquicia'), ('Tipo de producto', 'tipo'),
                                  ('Precio de venta', 'precio'), ('Costo de producción', 'costo'), ('Cantidad en inventario', 'inventario')]
        # Se recorren los campos para crear sus etiquetas y cajas de entrada.
        for fila, (texto, clave) in enumerate(etiquetas):
            # Se muestra el nombre del dato que debe introducirse.
            tk.Label(formulario, text=texto, bg='white', fg='#7a4300').grid(row=fila, column=0, sticky='w', pady=6)
            # Se crea la caja de texto y se guarda en el diccionario de campos.
            campos[clave] = ttk.Entry(formulario, width=35); campos[clave].grid(row=fila, column=1, sticky='w', pady=6)
            # Si se está editando, se colocan en la caja los datos que ya tenía el producto.
            if editar: campos[clave].insert(0, str(producto.get(clave, '')))
        # Guarda y valida los datos escritos en el formulario.
        def guardar():
            global siguiente_id
            
            # Se obtienen y limpian los tres datos de texto principales.
            nombre, franquicia, tipo = (campos[x].get().strip() for x in ('nombre', 'franquicia', 'tipo'))
            # Se verifica que los campos de texto obligatorios no estén vacíos.
            if not nombre or not franquicia or not tipo:
                # Se muestra una advertencia y se detiene el guardado.
                messagebox.showwarning('Datos', 'Faltan datos. Completa los campos de texto.'); return
            # Se intenta convertir precio, costo y cantidad a números válidos.
            try:
                # Se convierten los datos numéricos y se comprueba que sean válidos.
                precio = float(campos['precio'].get().replace(',', '.')); costo = float(campos['costo'].get().replace(',', '.')); cantidad = int(campos['inventario'].get())
                # No se permiten valores negativos ni un precio menor al costo.
                if precio < 0 or costo < 0 or cantidad < 0 or precio < costo: raise ValueError
            # Si alguna conversión o validación falla, se muestra una advertencia.
            except ValueError:
                # Se informa al usuario que debe revisar los datos numéricos.
                messagebox.showwarning('Datos', 'Revisa precio, costo y cantidad.'); return
            # Se agrupan los datos del formulario en un diccionario.
            datos = {'nombre': nombre, 'franquicia': franquicia, 'tipo': tipo, 'precio': precio, 'costo': costo, 'inventario': cantidad}
            # Si ya existía el producto, se actualizan sus datos.
            if editar:
                # update reemplaza la información anterior por la nueva.
                producto.update(datos)
            # Si es un producto nuevo, se crea su registro con sus valores iniciales.
            else:
                # Se agrega el producto con ID, ventas, ingresos, ganancia y estado activo iniciales.
                productos.append(datos | {'id': siguiente_id, 'vendidos': 0, 'ingresos': 0, 'ganancia': 0, 'activo': True}); siguiente_id += 1
            # Se guardan los datos, se regresa al inventario y se confirma la operación.
            guardar_datos(); self.inventario(); messagebox.showinfo('Inventario', 'Producto guardado correctamente.')
        # El botón ejecuta la función que valida y guarda el producto.
        self.boton(self.contenido, 'Guardar', guardar).pack(anchor='w', pady=10)
        # El botón permite cancelar y volver al inventario sin guardar cambios.
        self.boton(self.contenido, 'Cancelar', self.inventario, '#7f8c8d').pack(anchor='w')

    # Abre el formulario vacío para registrar un producto nuevo.
    def registrar_producto(self): self.formulario_producto()

    # Permite seleccionar un producto antes de modificarlo o eliminarlo.
    def seleccionar_producto(self, titulo, funcion):
        # Se obtienen los productos activos, se limpia la pantalla y se coloca el título indicado.
        lista = productos_activos(); self.limpiar(); self.titulo(titulo)
        # Si no existen productos activos, se informa al usuario y se termina la función.
        if not lista:
            # Se muestra el mensaje de que no hay productos disponibles.
            tk.Label(self.contenido, text='No hay productos registrados.', bg='#fff4e6', fg='#7a4300').pack(anchor='w'); return
        # Se recorre cada producto para crear un botón de selección.
        for p in lista:
            # El botón muestra el ID y nombre y envía ese producto a la función recibida.
            self.boton(self.contenido, f"ID {p['id']} - {p['nombre']}", lambda p=p: funcion(p)).pack(anchor='w', pady=2)

    # Permite elegir un producto y abrirlo en el formulario de modificación.
    def modificar_producto(self): self.seleccionar_producto('Modificar producto', self.formulario_producto)

    # Permite elegir un producto y marcarlo como inactivo.
    def eliminar_producto(self):
        # Define lo que ocurre con el producto elegido.
        def eliminar(p):
            # Se desactiva el producto, se guardan los datos, se vuelve al inventario y se muestra un aviso.
            p['activo'] = False; guardar_datos(); self.inventario(); messagebox.showinfo('Inventario', 'Producto eliminado del inventario.')
        # Se muestra la lista de productos para que el usuario elija uno.
        self.seleccionar_producto('Eliminar producto', eliminar)

    # Muestra todos los productos activos en una tabla de inventario.
    def inventario(self):
        # Se limpia la pantalla y se coloca el título de inventario.
        self.limpiar(); self.titulo('Inventario')
        # Se definen las claves que utilizarán las columnas de la tabla.
        columnas = ('id', 'nombre', 'franquicia', 'tipo', 'precio', 'costo', 'inventario', 'vendidos')
        # Se crea la tabla de Tkinter con las columnas definidas.
        tabla = ttk.Treeview(self.contenido, columns=columnas, show='headings')
        # Se recorre cada columna para asignar su encabezado visible y tamaño.
        for columna, nombre in zip(columnas, ['ID', 'Nombre', 'Franquicia', 'Tipo', 'Precio', 'Costo', 'Stock', 'Vendidos']):
            # Se establece el texto del encabezado y la alineación central de la columna.
            tabla.heading(columna, text=nombre); tabla.column(columna, width=105, anchor='center')
        # Se recorren los productos activos para llenar la tabla.
        for p in productos_activos():
            # Se inserta una fila con la información del producto y sus valores monetarios formateados.
            tabla.insert('', 'end', iid=str(p['id']), values=(p['id'], p['nombre'], p['franquicia'], p['tipo'], dinero(p['precio']), dinero(p['costo']), p['inventario'], p['vendidos']))
        # Se muestra la tabla ocupando el espacio disponible.
        tabla.pack(fill='both', expand=True)
        # Obtiene el producto correspondiente a la fila seleccionada.
        def seleccionado():
            # Se consulta qué fila está seleccionada en la tabla.
            s = tabla.selection()
            # Si no hay una fila seleccionada, se muestra una advertencia y se devuelve None.
            if not s: messagebox.showwarning('Inventario', 'Selecciona un producto de la tabla.'); return None
            # Se usa el ID de la fila para localizar el producto completo.
            return buscar_producto(int(s[0]))
        # Abre el producto seleccionado para modificarlo.
        def modificar():
            # Se obtiene el producto seleccionado.
            p = seleccionado()
            # Si existe un producto, se abre el formulario de edición.
            if p: self.formulario_producto(p)
        # Elimina el producto seleccionado del inventario activo.
        def eliminar():
            # Se obtiene el producto seleccionado.
            p = seleccionado()
            # Si existe, se marca como inactivo, se guardan los datos y se actualiza la pantalla.
            if p:
                # Se realiza la baja lógica del producto.
                p['activo'] = False; guardar_datos(); self.inventario()
        # Abre la pantalla para ajustar el stock del producto seleccionado.
        def ajustar():
            # Se obtiene el producto seleccionado.
            p = seleccionado()
            # Si existe, se abre el formulario de ajuste de existencias.
            if p: self.ajuste_producto(p)
        # Se crea el espacio inferior para los botones de gestión.
        botones = tk.Frame(self.contenido, bg='#fff4e6'); botones.pack(fill='x', pady=8)
        # Se agrega el botón para modificar el producto seleccionado.
        self.boton(botones, 'Modificar', modificar).pack(side='left', padx=3)
        # Se agrega el botón para eliminar el producto seleccionado.
        self.boton(botones, 'Eliminar', eliminar, '#c0392b').pack(side='left', padx=3)
        # Se agrega el botón para ajustar sus existencias.
        self.boton(botones, 'Ajustar stock', ajustar, '#2874a6').pack(side='left', padx=3)

    # Permite aumentar o disminuir manualmente las existencias de un producto.
    def ajuste_producto(self, producto):
        # Se limpia la pantalla y se muestra el título de ajuste.
        self.limpiar(); self.titulo('Ajustar existencias')
        # Se muestra el nombre del producto y su stock actual.
        tk.Label(self.contenido, text=f"{producto['nombre']}\nExistencias actuales: {producto['inventario']}", bg='#fff4e6', fg='#7a4300', font=('Arial', 12, 'bold')).pack(anchor='w', pady=10)
        # Se crea la caja donde se escribirá la cantidad que se agregará o retirará.
        entrada = ttk.Entry(self.contenido, width=20); entrada.pack(anchor='w', pady=8)
        # Aplica el cambio de existencias escrito por el usuario.
        def aplicar():
            # Se intenta convertir el texto introducido a entero.
            try:
                # Se obtiene el cambio de stock.
                cambio = int(entrada.get())
                # No se acepta cero ni un resultado final de inventario menor a cero.
                if cambio == 0 or producto['inventario'] + cambio < 0: raise ValueError
            # Si el valor es inválido, se muestra una advertencia y no se modifica el producto.
            except ValueError:
                # Se informa al usuario cuál es el error de la entrada.
                messagebox.showwarning('Stock', 'Escribe un número válido y no retires más del stock.'); return
            # Se aplica el cambio, se guarda la información y se regresa al inventario.
            producto['inventario'] += cambio; guardar_datos(); self.inventario()
        # El botón ejecuta el ajuste de existencias.
        self.boton(self.contenido, 'Aplicar', aplicar).pack(anchor='w', pady=5)
        # El botón cancela la operación y regresa al inventario.
        self.boton(self.contenido, 'Cancelar', self.inventario, '#7f8c8d').pack(anchor='w')

    # Muestra el formulario utilizado para registrar una venta.
    def registrar_venta(self):
        # Se obtienen los productos que todavía están activos.
        lista = productos_activos()
        # Si no hay productos, se informa que no es posible registrar la venta.
        if not lista:
            # Se muestra el aviso y termina la función.
            messagebox.showwarning('Venta', 'No hay productos disponibles para vender.'); return
        # Se limpia la pantalla y se coloca el título de la venta.
        self.limpiar(); self.titulo('Registrar venta')
        # Se crea el contenedor del formulario de venta.
        formulario = tk.Frame(self.contenido, bg='white', padx=20, pady=15); formulario.pack(fill='x')
        # Se muestra la etiqueta que identifica el campo del producto.
        tk.Label(formulario, text='ID del producto:', bg='white', fg='#7a4300').grid(row=0, column=0, sticky='w', pady=7)
        # Se crea la caja para introducir el ID y se coloca inicialmente el primer ID disponible.
        id_producto = ttk.Entry(formulario, width=20); id_producto.grid(row=0, column=1, sticky='w'); id_producto.insert(0, str(lista[0]['id']))
        # Se muestra la etiqueta para indicar la cantidad a vender.
        tk.Label(formulario, text='Cantidad:', bg='white', fg='#7a4300').grid(row=1, column=0, sticky='w', pady=7)
        # Se crea la caja de cantidad con 1 como valor inicial.
        cantidad = ttk.Entry(formulario, width=20); cantidad.grid(row=1, column=1, sticky='w'); cantidad.insert(0, '1')
        # Se muestra la etiqueta del descuento.
        tk.Label(formulario, text='Descuento (%):', bg='white', fg='#7a4300').grid(row=2, column=0, sticky='w', pady=7)
        # Se crea la caja de descuento con 0 como valor inicial.
        descuento = ttk.Entry(formulario, width=20); descuento.grid(row=2, column=1, sticky='w'); descuento.insert(0, '0')
        # Procesa la venta y actualiza los datos correspondientes.
        def vender():
            # Se intenta convertir ID, cantidad y descuento a sus tipos numéricos.
            try:
                # Se localiza el producto y se obtienen las cantidades introducidas por el usuario.
                producto = buscar_producto(int(id_producto.get())); unidades = int(cantidad.get()); porcentaje = float(descuento.get().replace(',', '.'))
                # Se valida que el producto exista, la cantidad sea positiva y el descuento esté entre 0 y 100.
                if not producto or unidades <= 0 or not 0 <= porcentaje <= 100: raise ValueError
            # Si alguno de los datos es incorrecto, se muestra una advertencia y se detiene la venta.
            except (ValueError, TypeError):
                # Se informa al usuario qué datos debe revisar.
                messagebox.showwarning('Venta', 'Revisa el ID, cantidad y descuento.'); return
            # Se verifica que el inventario disponible sea suficiente para cubrir la venta.
            if unidades > producto['inventario']:
                # Se muestra la advertencia y no se continúa con la venta.
                messagebox.showwarning('Venta', 'No hay suficientes unidades en inventario.'); return
            # Se calcula el precio con descuento, el ingreso y la ganancia de la venta.
            precio_final = producto['precio'] * (1 - porcentaje / 100); ingreso = precio_final * unidades; ganancia = (precio_final - producto['costo']) * unidades
            # Se descuenta el stock y se acumulan las unidades vendidas, ingresos y ganancias.
            producto['inventario'] -= unidades; producto['vendidos'] += unidades; producto['ingresos'] += ingreso; producto['ganancia'] += ganancia
            # Se agrega al historial el registro completo de la venta con fecha y resultados.
            ventas.append({'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'id_producto': producto['id'], 'producto': producto['nombre'], 'cantidad': unidades, 'precio_unitario': precio_final, 'descuento': porcentaje, 'ingreso': ingreso, 'ganancia': ganancia})
            # Se guardan los cambios, se actualiza el inventario y se muestra la confirmación.
            guardar_datos(); self.inventario(); messagebox.showinfo('Venta', 'Venta registrada correctamente.')
        # El botón ejecuta el proceso de venta.
        self.boton(self.contenido, 'Registrar venta', vender, '#2874a6').pack(anchor='w', pady=12)

    # Muestra las unidades vendidas y la clasificación de demanda de cada producto activo.
    def analisis_demanda(self):
        # Se limpia la pantalla y se coloca el título correspondiente.
        self.limpiar(); self.titulo('Análisis de demanda')
        # Se obtiene la lista de productos activos.
        lista = productos_activos()
        # Si no hay productos, se informa al usuario y se termina la función.
        if not lista:
            # Se muestra el mensaje de ausencia de productos.
            tk.Label(self.contenido, text='No hay productos para analizar.', bg='#fff4e6', fg='#7a4300').pack(anchor='w'); return
        # Se recorre cada producto activo para mostrar sus ventas y demanda.
        for p in lista:
            # Se muestra el nombre, número de vendidos y clasificación de demanda del producto.
            tk.Label(self.contenido, text=f"{p['nombre']} | Vendidos: {p['vendidos']} | Demanda: {demanda(p)}", bg='white', fg='#7a4300', anchor='w', padx=10, pady=9).pack(fill='x', pady=2)

    # Muestra todas las ventas registradas y sus datos principales.
    def historial_ventas(self):
        # Se limpia la pantalla y se muestra el título del historial.
        self.limpiar(); self.titulo('Historial de ventas')
        # Se definen las claves de las columnas de la tabla del historial.
        columnas = ('fecha', 'id', 'producto', 'cantidad', 'precio', 'descuento', 'ingreso')
        # Se crea la tabla donde aparecerán las ventas.
        tabla = ttk.Treeview(self.contenido, columns=columnas, show='headings')
        # Se asignan nombres visibles y ancho a cada columna.
        for columna, nombre in zip(columnas, ['Fecha', 'ID', 'Producto', 'Cantidad', 'Precio', 'Descuento', 'Ingreso']):
            # Se configura el encabezado y la alineación de la columna.
            tabla.heading(columna, text=nombre); tabla.column(columna, width=110, anchor='center')
        # Se recorre la lista invertida para mostrar primero la venta más reciente.
        for v in reversed(ventas):
            # Se agrega cada venta como una fila de la tabla con los valores formateados.
            tabla.insert('', 'end', values=(v.get('fecha', ''), v.get('id_producto', ''), v.get('producto', ''), v.get('cantidad', 0), dinero(v.get('precio_unitario', 0)), f"{v.get('descuento', 0)}%", dinero(v.get('ingreso', 0))))
        # Se muestra la tabla ocupando el espacio disponible.
        tabla.pack(fill='both', expand=True)

# Crea la ventana principal y mantiene activa la aplicación.
def abrir_programa():
    # Se crea la ventana, se construye la clase Programa dentro de ella y se inicia el bucle de Tkinter.
    ventana = tk.Tk(); Programa(ventana); ventana.mainloop()

# Se cargan los datos existentes antes de pedir las credenciales.
cargar_datos()
# Se inicia la pantalla de inicio de sesión del programa.
iniciar_sesion()
