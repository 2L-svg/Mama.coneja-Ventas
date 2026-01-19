import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('mama_coneja.db')
c = conn.cursor()

#Inicializar tablas
c.executescript("""
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS ventas;

CREATE TABLE categorias (
    id INTEGER PRIMARY KEY,
    nombre TEXT
);

CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria_id INTEGER,
    precio REAL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    ciudad TEXT
);

CREATE TABLE ventas (
    id INTEGER PRIMARY KEY,
    fecha TEXT,
    producto_id INTEGER,
    cliente_id INTEGER,
    cantidad INTEGER,
    total REAL,
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
""")

#Se insertan las categorias
categorias = ['lacteos', 'despensa', 'bebidas', 'limpieza', 'panaderia']

for i, cat in enumerate(categorias, start=1):
    c.execute("INSERT INTO categorias (id, nombre) VALUES (?, ?)", (i, cat))

#Apartado para productos
productos = [
    ('Leche entera', 1, 22),
    ('Arroz 1kg', 2, 30),
    ('Refresco 2L', 3, 22),
]

for i, p in enumerate(productos, start=1):
    c.execute("INSERT INTO productos (id, nombre, categoria_id, precio) VALUES (?,?,?,?)",
              (i, p[0], p[1], p[2]))

#Tienda de clientes
ciudades = ['Mazatlán', 'Oaxaca', 'México']

for i in range(1, 21):
    c.execute("INSERT INTO clientes (id, nombre, ciudad) VALUES (?, ?, ?)",
              (i, f'cliente_{i}', random.choice(ciudades)))

#Generacion de ventas
start = datetime(2025, 1, 1)

for i in range(1, 1001):
    fecha = start + timedelta(days=random.randint(0, 180))
    producto_id = random.randint(1, len(productos))
    cliente_id = random.randint(1, 20)
    cantidad = random.randint(1, 5)

    c.execute("SELECT precio FROM productos WHERE id=?", (producto_id,))
    precio = c.fetchone()[0]

    total = round(precio * cantidad, 2)

    c.execute("""INSERT INTO ventas (fecha, producto_id, cliente_id, cantidad, total)
                 VALUES (?, ?, ?, ?, ?)""",
              (fecha.strftime('%Y-%m-%d'), producto_id, cliente_id, cantidad, total))

conn.commit()
conn.close()
print("Base de datos Mama Coneja creada correctamente.")
