import sqlite3

conexion = sqlite3.connect('BaseDeDatos.db')
cursorTB = conexion.cursor()

cursorTB.execute('''CREATE TABLE IF NOT EXISTS tabla_precios(
    id INTEGER PRIMARY KEY,

)''')


cursorTB.execute("INSERT INTO productos VALUES (NULL, ?, ?, ?)", ())

todos_productos = [
   
]

cursorTB.executemany("INSERT INTO productos VALUES (NULL, ?, ?, ?)", todos_productos)

conexion.commit()
conexion.close()