import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import tkinter as tk

# === funcion para consultar precios ==================================================================================
def consultar_precio():
    tabla = combo_tabla.get()
    bolsa = entry_nombre.get().strip().upper()

    if not tabla or not bolsa:
        messagebox.showerror("Error", "Selecciona la tabla y escribe el nombre de la bolsa.")
        return

    conn = sqlite3.connect("productos.db")
    cur = conn.cursor()
    cur.execute(f"""
        SELECT id, bolsa, kraft, bond, couche, cartulina
        FROM {tabla}
        WHERE bolsa = ?
    """, (bolsa,))
    fila = cur.fetchone()
    conn.close()

    lista.delete(0, "end")
    if fila:
        global id_actual
        id_actual = fila[0]
        entry_kraft.delete(0, "end")
        entry_bond.delete(0, "end")
        entry_couche.delete(0, "end")
        entry_cartulina.delete(0, "end")
        entry_kraft.insert(0, fila[2])
        entry_bond.insert(0, fila[3])
        entry_couche.insert(0, fila[4])
        entry_cartulina.insert(0, fila[5])
        lista.insert("end", f"Bolsa: {fila[1]}")
        lista.insert("end", f"KRAFT: ${fila[2]}")
        lista.insert("end", f"BOND: ${fila[3]}")
        lista.insert("end", f"COUCHE: ${fila[4]}")
        lista.insert("end", f"CARTULINA: ${fila[5]}")
    else:
        messagebox.showinfo("No encontrado", f"No se encontró '{bolsa}' en la tabla '{tabla}'.")

# === funciones para editar=========================================================================================
def guardar_edicion():
    tabla = combo_tabla.get()
    if not id_actual:
        messagebox.showerror("Error", "Primero consulta un producto para editar.")
        return
    try:
        kraft = float(entry_kraft.get())
        bond = float(entry_bond.get())
        couche = float(entry_couche.get())
        cartulina = float(entry_cartulina.get())
    except ValueError:
        messagebox.showerror("Error", "Todos los precios deben ser numéricos.")
        return

    conn = sqlite3.connect("productos.db")
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE {tabla}
        SET kraft = ?, bond = ?, couche = ?, cartulina = ?
        WHERE id = ?
    """, (kraft, bond, couche, cartulina, id_actual))
    conn.commit()
    conn.close()
    messagebox.showinfo("Actualizado", "Producto actualizado correctamente.")
    consultar_precio()

# === Función para eliminar =======================================================================================
def eliminar_producto():
    tabla = combo_tabla.get()
    bolsa = entry_nombre.get().strip().upper()
    if not bolsa:
        messagebox.showerror("Error", "Escribe el nombre de la bolsa que deseas eliminar.")
        return

    conn = sqlite3.connect("productos.db")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {tabla} WHERE bolsa = ?", (bolsa,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Eliminado", f"'{bolsa}' eliminado de '{tabla}'.")
    lista.delete(0, "end")
    entry_kraft.delete(0, "end")
    entry_bond.delete(0, "end")
    entry_couche.delete(0, "end")
    entry_cartulina.delete(0, "end")

# === Interfaz grafica ==============================================================================================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Consultar, Editar y Eliminar Precios")
app.geometry("600x650")

id_actual = None

combo_tabla = ctk.CTkComboBox(app, values=["medio_mayoreo", "menudeo"])
combo_tabla.pack(pady=10)
combo_tabla.set("medio_mayoreo")

entry_nombre = ctk.CTkEntry(app, placeholder_text="Nombre de la bolsa (ej. MINI 1)")
entry_nombre.pack(pady=10, padx=10)

btn_buscar = ctk.CTkButton(app, text="Consultar Precio", command=consultar_precio)
btn_buscar.pack(pady=5)

# === entrada de precios=============================================================================================
entry_kraft = ctk.CTkEntry(app, placeholder_text="Precio KRAFT")
entry_kraft.pack(pady=2, padx=10)

entry_bond = ctk.CTkEntry(app, placeholder_text="Precio BOND")
entry_bond.pack(pady=2, padx=10)

entry_couche = ctk.CTkEntry(app, placeholder_text="Precio COUCHE")
entry_couche.pack(pady=2, padx=10)

entry_cartulina = ctk.CTkEntry(app, placeholder_text="Precio CARTULINA")
entry_cartulina.pack(pady=2, padx=10)

# === Botones de comandos==============================================================================================
frame_botones = ctk.CTkFrame(app)
frame_botones.pack(pady=10)

btn_guardar = ctk.CTkButton(frame_botones, text="Guardar Cambios", command=guardar_edicion)
btn_guardar.grid(row=0, column=0, padx=10)

btn_eliminar = ctk.CTkButton(frame_botones, text="Eliminar Bolsa", command=eliminar_producto)
btn_eliminar.grid(row=0, column=1, padx=10)

# === lista de resultados=============================================================================================
frame_lista = ctk.CTkFrame(app)
frame_lista.pack(pady=10, padx=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side="right", fill="y")

lista = tk.Listbox(frame_lista, font=("Segoe UI", 12), yscrollcommand=scrollbar.set, height=15, selectbackground="#007acc")
lista.pack(side="left", fill="both", expand=True)
scrollbar.config(command=lista.yview)


app.mainloop()