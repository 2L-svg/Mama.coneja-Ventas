import pandas as pd
import sqlite3

conn = sqlite3.connect('mama_coneja.db')
df = pd.read_sql_query("SELECT v.*, p.nombre as producto, p.precio, c.nombre as categoria_id_nombre, cat.nombre as categoria FROM ventas v JOIN productos p ON v.producto_id=p.id JOIN categorias cat ON p.categoria_id=cat.id JOIN clientes c ON v.cliente_id=c.id", conn, parse_dates=['fecha'])
conn.close()

# Columnas de tiempo
df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month
df['dia'] = df['fecha'].dt.day
df['dia_semana'] = df['fecha'].dt.day_name()

# Revisar nulos y duplicados
print("Nulos por columna:\n", df.isnull().sum())
print("Duplicados:", df.duplicated().sum())

# Estadísticas básicas
print(df.describe(include='all'))

# Top 10 productos por ventas (cantidad)
top_productos = df.groupby('producto').agg({'cantidad':'sum','total':'sum'}).sort_values('cantidad',ascending=False).head(10)
print(top_productos)
