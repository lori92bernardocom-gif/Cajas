import sqlite3

def inicializar_bd():
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()

    # Tabla para las cotizaciones (datos del cliente)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cotizaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT,
            cliente TEXT,
            whatsapp TEXT,
            anticipo REAL,
            forma_pago TEXT,
            fecha TEXT,
            vendedor TEXT,
            total REAL
        )
    """)

    # Tabla para detalle de productos por cotización
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_cotizacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cotizacion_id INTEGER,
            producto TEXT,
            papel TEXT,
            cantidad INTEGER,
            precio REAL,
            total REAL,
            FOREIGN KEY (cotizacion_id) REFERENCES cotizaciones(id)
        )
    """)

    conn.commit()
    conn.close()

inicializar_bd()
