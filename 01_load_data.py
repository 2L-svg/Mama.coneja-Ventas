import pandas as pd
import sqlite3

conn = sqlite3.connect('mama_coneja.db')

df_ventas = pd.read_sql_query("SELECT * FROM ventas", conn, parse_dates=['fecha'])
df_productos = pd.read_sql_query("SELECT * FROM productos", conn)
df_categorias = pd.read_sql_query("SELECT * FROM categorias", conn)
df_clientes = pd.read_sql_query("SELECT * FROM clientes", conn)

conn.close()

print(df_ventas.head())
print(df_productos.head())
