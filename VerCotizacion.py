import sqlite3
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox

def abrir_consultas():
    # Ventana secundaria ligada a la principal
    app = ctk.CTk()
    app.title("Consulta de Cotizaciones")
    app.geometry("1000x600")

    # ================== FRAME BÚSQUEDA ==================
    frame_busqueda = ctk.CTkFrame(app)
    frame_busqueda.pack(fill="x", padx=10, pady=10)

    lbl_buscar = ctk.CTkLabel(frame_busqueda, text="Buscar por Cliente o Fecha:")
    lbl_buscar.pack(side="left", padx=10)

    entry_buscar = ctk.CTkEntry(frame_busqueda, width=300)
    entry_buscar.pack(side="left", padx=10)

    # Botón buscar
    def buscar():
        cargar_cotizaciones(entry_buscar.get())
    btn_buscar = ctk.CTkButton(frame_busqueda, text="Buscar", command=buscar)
    btn_buscar.pack(side="left", padx=10)

    # ================== TREEVIEW COTIZACIONES ==================
    frame_tabla = ctk.CTkFrame(app)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    tabla_cotizaciones = ttk.Treeview(
        frame_tabla,
        columns=("id","marca","cliente","whatsapp","anticipo","forma_pago","fecha","vendedor","total"),
        show="headings",
        height=15
    )

    encabezados = ["ID","Marca","Cliente","WhatsApp","Anticipo","Forma Pago","Fecha","Vendedor","Total"]
    for col, text in zip(tabla_cotizaciones["columns"], encabezados):
        tabla_cotizaciones.heading(col, text=text)
        tabla_cotizaciones.column(col, anchor="center", width=100)

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_cotizaciones.yview)
    tabla_cotizaciones.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla_cotizaciones.pack(fill="both", expand=True)

    # ================== TREEVIEW DETALLE ==================
    frame_detalle = ctk.CTkFrame(app)
    frame_detalle.pack(fill="both", expand=True, padx=10, pady=10)

    tabla_detalle = ttk.Treeview(
        frame_detalle,
        columns=("producto","papel","cantidad","precio","total"),
        show="headings",
        height=8
    )

    encabezados_detalle = ["Producto","Papel","Cantidad","Precio","Total"]
    for col, text in zip(tabla_detalle["columns"], encabezados_detalle):
        tabla_detalle.heading(col, text=text)
        tabla_detalle.column(col, anchor="center", width=120)

    scrollbar_det = ttk.Scrollbar(frame_detalle, orient="vertical", command=tabla_detalle.yview)
    tabla_detalle.configure(yscrollcommand=scrollbar_det.set)
    scrollbar_det.pack(side="right", fill="y")
    tabla_detalle.pack(fill="both", expand=True)

    # ================== FUNCIONES INTERNAS ==================
    def cargar_cotizaciones(filtro=""):
        conn = sqlite3.connect("productos.db")
        cursor = conn.cursor()
        if filtro:
            cursor.execute("""
                SELECT * FROM cotizaciones 
                WHERE cliente LIKE ? OR fecha LIKE ?
                ORDER BY fecha DESC
            """, (f"%{filtro}%", f"%{filtro}%"))
        else:
            cursor.execute("SELECT * FROM cotizaciones ORDER BY fecha DESC")
        rows = cursor.fetchall()
        conn.close()

        # Limpiar tabla
        for row in tabla_cotizaciones.get_children():
            tabla_cotizaciones.delete(row)
        for row in rows:
            tabla_cotizaciones.insert("", "end", values=row)

    def cargar_detalle(event):
        seleccion = tabla_cotizaciones.selection()
        if not seleccion:
            return
        cotizacion_id = tabla_cotizaciones.item(seleccion[0])["values"][0]

        conn = sqlite3.connect("productos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT producto,papel,cantidad,precio,total FROM detalle_cotizacion WHERE cotizacion_id=?", (cotizacion_id,))
        rows = cursor.fetchall()
        conn.close()

        # Limpiar detalle
        for row in tabla_detalle.get_children():
            tabla_detalle.delete(row)
        for row in rows:
            tabla_detalle.insert("", "end", values=row)

    def eliminar_cotizacion():
        seleccion = tabla_cotizaciones.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una cotización para eliminar.")
            return

        cotizacion_id = tabla_cotizaciones.item(seleccion[0])["values"][0]

        confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar la cotización ID {cotizacion_id}?")
        if not confirmar:
            return

        conn = sqlite3.connect("productos.db")
        cursor = conn.cursor()

        # Primero eliminar detalle
        cursor.execute("DELETE FROM detalle_cotizacion WHERE cotizacion_id=?", (cotizacion_id,))
        # Luego eliminar la cotización
        cursor.execute("DELETE FROM cotizaciones WHERE id=?", (cotizacion_id,))
        
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Cotización ID {cotizacion_id} eliminada correctamente.")

        cargar_cotizaciones()

        # limpiar tabla detalle
        for row in tabla_detalle.get_children():
            tabla_detalle.delete(row)

    # ================== BOTÓN ELIMINAR ==================
    btn_eliminar = ctk.CTkButton(app, text="Eliminar Cotización", fg_color="red", hover_color="darkred", command=eliminar_cotizacion)
    btn_eliminar.pack(pady=10)

    # ================== BINDINGS ==================
    tabla_cotizaciones.bind("<<TreeviewSelect>>", cargar_detalle)

    # ================== CARGAR INICIAL ==================
    cargar_cotizaciones()
    app.mainloop()

abrir_consultas()
