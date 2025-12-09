import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import subprocess
from tkinter import ttk



# ==================== FUNCIONES ========================================================================================

def cargar_productos(tabla="medio_mayoreo", papel="cartulina"):
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT bolsa, {papel} FROM {tabla}")
    datos = cursor.fetchall()
    conn.close()
    return dict(datos)

def agregar_producto():
    producto = combo_producto.get()
    cantidad = entry_cantidad.get()
    tipo_papel = combo_papel.get()
    tintas = combo_tintas.get()
    plastificado = combo_plastificado.get()
    letras = combo_letras.get()
    listones = combo_listones.get()
    
    if not producto or not cantidad or tipo_papel == "Selecciona tipo de papel":
        messagebox.showwarning("Campos vacíos", "Selecciona un producto, tipo de papel y cantidad.")
        return

    try:
        cantidad = int(cantidad)
    except ValueError:
        messagebox.showerror("Error", "La cantidad debe ser un número.")
        return

    try:
        productos_por_papel = cargar_productos(papel=tipo_papel)
        precio = productos_por_papel[producto]
    except KeyError:
        messagebox.showerror("Error", f"No se encontró el producto '{producto}' con papel '{tipo_papel}'.")
        return
    except sqlite3.OperationalError:
        messagebox.showerror("Error", f"No se encontró la columna '{tipo_papel}' en la base de datos.")
        return

    total = precio * cantidad
    items_cotizados.append((producto, tipo_papel, cantidad, precio, total, tintas, plastificado, letras, listones))

    tabla.insert(
        "",
        "end",
        values=(
            producto,
            tipo_papel,
            cantidad,
            f"${precio:,.2f}",
            tintas,
            plastificado,
            letras,
            listones,
            f"${total:,.2f}",
        ),
    )

    entry_cantidad.delete(0, "end")
    actualizar_total()

def actualizar_total():
    total = sum(item[4] for item in items_cotizados)
    piezas = sum(item[2] for item in items_cotizados)
    label_total.configure(text=f"Piezas: {piezas}   |   Gran Total: ${total:,.2f}")

def abrir_admin():
    subprocess.Popen(["python", "2_admin_productos.py"])

def abrir_consultas():
    subprocess.Popen(["python", "VerCotizacion.py"])



def guardar_cotizacion():
    # Datos cliente
    marca = entry_marca.get()
    cliente = entry_nombre.get()
    whatsapp = entry_whatsapp.get()
    anticipo = entry_anticipo.get()
    forma_pago = combo_pago.get()
    fecha = entry_fecha.get()
    vendedor = entry_vendedor.get()

    # Validar
    if not cliente or not fecha:
        messagebox.showwarning("Campos requeridos", "Debes llenar al menos Nombre Cliente y Fecha.")
        return

    try:
        anticipo = float(anticipo) if anticipo else 0.0
    except ValueError:
        messagebox.showerror("Error", "El anticipo debe ser un número válido.")
        return

    total = sum(item[4] for item in items_cotizados)

    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()

    # Guardar datos generales
    cursor.execute("""
        INSERT INTO cotizaciones (marca, cliente, whatsapp, anticipo, forma_pago, fecha, vendedor, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (marca, cliente, whatsapp, anticipo, forma_pago, fecha, vendedor, total))

    cotizacion_id = cursor.lastrowid  # ID de la cotización recién creada

    # Guardar detalle de productos
    for item in items_cotizados:
        producto, papel, cantidad, precio, total_item = item
        cursor.execute("""
            INSERT INTO detalle_cotizacion (cotizacion_id, producto, papel, cantidad, precio, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cotizacion_id, producto, papel, cantidad, precio, total_item))

    conn.commit()
    conn.close()

    messagebox.showinfo("Éxito", "Cotización y productos guardados en la base de datos.")


# ==================== UI INICIAL ===================================================================================================

ctk.set_appearance_mode("light")    
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Cotizador de Productos     Created by Bernardo Sabino")
app.geometry("1200x700")

# ==================== DATOS =======================================================================================================

productos = cargar_productos()
items_cotizados = []

# ==================== UI ==============================================================================================================

# --- Frame principal dividido en arriba (inputs) y abajo (tabla)
frame_superior_contenedor = ctk.CTkFrame(app)
frame_superior_contenedor.pack(fill="x", padx=20, pady=10)

# Frame izquierda (datos cliente)
frame_vertical = ctk.CTkFrame(frame_superior_contenedor, width=400)
frame_vertical.pack(side="left", padx=10, pady=10, fill="y")

label_cliente = ctk.CTkLabel(frame_vertical, text="Datos del Cliente", font=("Arial", 12, "bold"))
label_cliente.pack(pady=10)

# Aquí luego puedes agregar Entry para Nombre, Teléfono, etc.
# Marca
lbl_marca = ctk.CTkLabel(frame_vertical, text="Marca:")
lbl_marca.pack(anchor="w", padx=10)
entry_marca = ctk.CTkEntry(frame_vertical, placeholder_text="Marca")
entry_marca.pack(padx=10, pady=5, fill="x")

# Nombre Cliente
lbl_nombre = ctk.CTkLabel(frame_vertical, text="Nombre Cliente:")
lbl_nombre.pack(anchor="w", padx=10)
entry_nombre = ctk.CTkEntry(frame_vertical, placeholder_text="Nombre del Cliente")
entry_nombre.pack(padx=10, pady=5, fill="x")

# WhatsApp
lbl_whatsapp = ctk.CTkLabel(frame_vertical, text="WhatsApp:")
lbl_whatsapp.pack(anchor="w", padx=10)
entry_whatsapp = ctk.CTkEntry(frame_vertical, placeholder_text="Número WhatsApp")
entry_whatsapp.pack(padx=10, pady=5, fill="x")

# Anticipo
lbl_anticipo = ctk.CTkLabel(frame_vertical, text="Anticipo:")
lbl_anticipo.pack(anchor="w", padx=10)
entry_anticipo = ctk.CTkEntry(frame_vertical, placeholder_text="Monto de anticipo")
entry_anticipo.pack(padx=10, pady=5, fill="x")

# Forma de Pago
lbl_pago = ctk.CTkLabel(frame_vertical, text="Forma de Pago:")
lbl_pago.pack(anchor="w", padx=10)
combo_pago = ctk.CTkComboBox(frame_vertical, values=["Efectivo", "Transferencia", "Tarjeta", "Otro"])
combo_pago.set("Selecciona")
combo_pago.pack(padx=10, pady=5, fill="x")

# Fecha
lbl_fecha = ctk.CTkLabel(frame_vertical, text="Fecha:")
lbl_fecha.pack(anchor="w", padx=10)
entry_fecha = ctk.CTkEntry(frame_vertical, placeholder_text="DD/MM/AAAA")
entry_fecha.pack(padx=10, pady=5, fill="x")

# Vendedor
lbl_vendedor = ctk.CTkLabel(frame_vertical, text="Vendedor:")
lbl_vendedor.pack(anchor="w", padx=10)
entry_vendedor = ctk.CTkEntry(frame_vertical, placeholder_text="Nombre del vendedor")
entry_vendedor.pack(padx=10, pady=5, fill="x")



# Frame derecha (selección productos)
frame_superior = ctk.CTkFrame(frame_superior_contenedor)
frame_superior.pack(side="left", padx=20, pady=10, fill="both", expand=True)

for col in range(4):
    frame_superior.grid_columnconfigure(col, weight=1)


label_producto = ctk.CTkLabel(frame_superior, text="Producto (Bolsa o Caja):", font=("Arial", 14))
label_producto.grid(row=0, column=0, padx=10, pady=(10, 0))
combo_producto = ctk.CTkComboBox(frame_superior, values=list(productos.keys()), width=250)
combo_producto.set("Selecciona una Bolsa o Caja")
combo_producto.grid(row=1, column=0, padx=10)

label_papel = ctk.CTkLabel(frame_superior, text="Tipo Papel:", font=("Arial", 14))
label_papel.grid(row=0, column=1, padx=10, pady=(10, 0))
combo_papel = ctk.CTkComboBox(frame_superior, values=["kraft", "bond", "couche", "cartulina"], width=200)
combo_papel.set("Selecciona tipo de papel")
combo_papel.grid(row=1, column=1, padx=10)

label_cantidad = ctk.CTkLabel(frame_superior, text="Cantidad:", font=("Arial", 14))
label_cantidad.grid(row=0, column=2, padx=10, pady=(10, 0))
entry_cantidad = ctk.CTkEntry(frame_superior, placeholder_text="Cantidad")
entry_cantidad.grid(row=1, column=2, padx=10)

label_tintas = ctk.CTkLabel(frame_superior, text="Tintas:", font=("Arial", 14))
label_tintas.grid(row=2, column=0, padx=10, pady=(10, 0))
combo_tintas = ctk.CTkComboBox(frame_superior, values=["1", "2", "3", "4"], width=150)
combo_tintas.set("1")
combo_tintas.grid(row=3, column=0, padx=10)

label_plastificado = ctk.CTkLabel(frame_superior, text="Plastificado:", font=("Arial", 14))
label_plastificado.grid(row=2, column=1, padx=10, pady=(10, 0))
combo_plastificado = ctk.CTkComboBox(frame_superior, values=["Sí", "No"], width=150)
combo_plastificado.set("No")
combo_plastificado.grid(row=3, column=1, padx=10)

label_letras = ctk.CTkLabel(frame_superior, text="Letras Metálicas:", font=("Arial", 14))
label_letras.grid(row=2, column=2, padx=10, pady=(10, 0))
combo_letras = ctk.CTkComboBox(frame_superior, values=["1", "N/A"], width=150)
combo_letras.set("N/A")
combo_letras.grid(row=3, column=2, padx=10)

label_listones = ctk.CTkLabel(frame_superior, text="Listones:", font=("Arial", 14))
label_listones.grid(row=2, column=3, padx=10, pady=(10, 0))
combo_listones = ctk.CTkComboBox(frame_superior, values=["Listo", "Media Luna"], width=150)
combo_listones.set("Listo")
combo_listones.grid(row=3, column=3, padx=10)


btn_agregar = ctk.CTkButton(frame_superior, text="Generar cotización", command=agregar_producto)
btn_agregar.grid(row=5, column=0, pady=20, padx=10, sticky="ew")

btn_admin = ctk.CTkButton(frame_superior, text="Administrar productos", command=abrir_admin)
btn_admin.grid(row=5, column=1, pady=20, padx=10, sticky="ew")

btn_guardar = ctk.CTkButton(frame_superior, text="Guardar Cotización", command=guardar_cotizacion)
btn_guardar.grid(row=5, column=2, pady=20, padx=10, sticky="ew")

btn_consultar = ctk.CTkButton(frame_superior, text="Consultar Cotizaciones", command=abrir_consultas)
btn_consultar.grid(row=5, column=3, pady=20, padx=10, sticky="ew")

# --- Frame para la tabla (abajo)
frame_tabla = ctk.CTkFrame(app)
frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

tabla = ttk.Treeview(
    frame_tabla,
    columns=("producto","papel", "cantidad", "precio", "tintas", "plastificado", "letras", "listones","total"),
    show="headings",
    height=10)
tabla.pack(side="left", fill="both", expand=True)

style = ttk.Style()
style.configure("Treeview", font=("Arial", 11), rowheight=24)
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

#  Encabezados
tabla.heading("producto", text="Producto")
tabla.heading("papel", text="Papel")
tabla.heading("cantidad", text="Piezas")
tabla.heading("precio", text="Precio Base")
tabla.heading("total", text="Total")
tabla.heading("tintas", text="Tintas")
tabla.heading("plastificado", text="Plastificado")
tabla.heading("letras", text="Letras Metálicas")
tabla.heading("listones", text="Listones")


# Ancho de columnas
tabla.column("producto", width=200, anchor="center")
tabla.column("papel", width=120, anchor="center")
tabla.column("cantidad", width=100, anchor="center")
tabla.column("precio", width=140, anchor="center")
tabla.column("total", width=140, anchor="center")
tabla.column("tintas", width=90, anchor="center")
tabla.column("plastificado", width=120, anchor="center")
tabla.column("letras", width=140, anchor="center")
tabla.column("listones", width=140, anchor="center")

# Scrollbar
scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")


# Label total (piezas + dinero)
label_total = ctk.CTkLabel(app, text="Piezas: 0   |   Gran Total: $0.00", font=("Segoe UI", 16))
label_total.pack(pady=10)

app.mainloop()
