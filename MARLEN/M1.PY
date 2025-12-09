import sqlite3

conexion = sqlite3.connect('BaseDeDatos.db')
cursorTB = conexion.cursor()

cursorTB.execute('''CREATE TABLE IF NOT EXISTS productos(
    id INTEGER PRIMARY KEY,
    BOLASAS TEXT,
    KRAFT INTEGER,
    BOND INTEGER
)''')


cursorTB.execute("INSERT INTO productos VALUES (NULL, ?, ?, ?)", ('MINI 1', 5.9, 5.55))

todos_productos = [
    ('MINI1', 5.09, 5.55),
    ('MINI2', 5.50, 6.33),
    ('CHICA 1', 5.91, 6.51),
    ('CHICA 2', 6.20, 6.97),
    ('CHICA 3', 6.16, 6.07),
    ('UNITALLA', 6.76, 7.92),
    ('MEDIANA', 6.55, 7.71),
    ('GRANDE H', 8.66, 9.86 ),
    ('GRANDE V', 8.41, 9.66),
    ('JUMBO H', 9.46, 11.67),
    ('JUMBO VERTICAL', 13.02, 16.51),
    ('CAJA CHICA', 13.23, 13.23),
    ('CAJA MEDIANA', 21.37, 21.37),
    ('CAJA GRANDE', 25.35, 25.35),
    ('CAJA GORRA', 11.24, 11.24)
]

cursorTB.executemany("INSERT INTO productos VALUES (NULL, ?, ?, ?)", todos_productos)

conexion.commit()
conexion.close()