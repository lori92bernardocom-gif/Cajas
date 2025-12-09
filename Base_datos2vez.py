import sqlite3


conn = sqlite3.connect("productos.db")
cursor = conn.cursor()

# medio_mayoreo
cursor.execute("""
CREATE TABLE IF NOT EXISTS medio_mayoreo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bolsa TEXT,
    kraft REAL,
    bond REAL,
    couche REAL,
    cartulina REAL
)
""")

# tabla menudeo
cursor.execute("""
CREATE TABLE IF NOT EXISTS menudeo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bolsa TEXT,
    kraft REAL,
    bond REAL,
    couche REAL,
    cartulina REAL
)
""")
# si lo vuelves a ejecutar no pasa nada, ya que solo se encima la informacion en las tablas ya creadas
# la idea es hacer un lay out para cargarlas a travez de un excel en lugar de codigo
# Datos para medio_mayoreo
medio_mayoreo = [
    ("MINI 1", 5.09, 5.55, 7.98, 6.03),
    ("MINI 2", 5.50, 6.33, 9.79, 6.80),
    ("CHICA 1", 5.91, 6.51, 9.26, 9.94),
    ("CHICA 2", 6.20, 6.97, 10.62, 7.78),
    ("CHICA 3", 6.16, 6.07, 10.25, 7.75),
    ("UNITALLA", 6.76, 7.92, 12.52, 9.13),
    ("MEDIANA", 6.55, 7.71, 12.12, 8.92),
    ("GRANDE H", 8.66, 9.86, 16.74, 11.97),
    ("GRANDE V", 8.41, 9.66, 16.51, 11.69),
    ("JUMBO H", 9.46, 11.67, 19.93, 13.98),
    ("JUMBO VERTICAL", 13.02, 16.51, 29.22, 20.34),
    ("CAJA CHICA", 13.23, 13.23, 13.23, 13.23),
    ("CAJA MEDIANA", 21.37, 21.37, 21.37, 21.37),
    ("CAJA GRANDE", 25.35, 25.35, 25.35, 25.35),
    ("CAJA GORRA", 11.24, 11.24, 11.24, 11.24)
]

# Datos para menudeo
menudeo = [
    ("MINI 1", 3.41, 3.73, 5.35, 4.06),
    ("MINI 2", 3.84, 4.45, 6.96, 4.80),
    ("CHICA 1", 4.09, 4.58, 6.54, 7.30),
    ("CHICA 2", 4.32, 4.94, 7.67, 5.58),
    ("CHICA 3", 4.29, 4.50, 7.36, 5.55),
    ("UNITALLA", 5.07, 5.99, 9.55, 6.95),
    ("MEDIANA", 4.89, 5.81, 9.22, 6.77),
    ("GRANDE H", 6.72, 7.70, 13.46, 9.45),
    ("GRANDE V", 6.37, 7.37, 12.89, 8.98),
    ("JUMBO H", 7.38, 9.20, 16.19, 11.11),
    ("JUMBO VERTICAL", 10.33, 13.20, 24.19, 16.36),
    ("CAJA CHICA", 11.03, 11.03, 11.03, 11.03),
    ("CAJA MEDIANA", 17.81, 17.81, 17.81, 17.81),
    ("CAJA GRANDE", 21.12, 21.12, 21.12, 21.12),
    ("CAJA GORRA", 9.37, 9.37, 9.37, 9.37)
]

# Insertar datos
cursor.executemany("INSERT INTO medio_mayoreo (bolsa, kraft, bond, couche, cartulina) VALUES (?, ?, ?, ?, ?)", medio_mayoreo)
cursor.executemany("INSERT INTO menudeo (bolsa, kraft, bond, couche, cartulina) VALUES (?, ?, ?, ?, ?)", menudeo)

# Guardar y cerrar
conn.commit()
conn.close()
