import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('mama_coneja.db')
df = pd.read_sql_query("SELECT v.*, p.nombre as producto, p.precio, cat.nombre as categoria FROM ventas v JOIN productos p ON v.producto_id=p.id JOIN categorias cat ON p.categoria_id=cat.id", conn, parse_dates=['fecha'])
conn.close()

df['mes_ano'] = df['fecha'].dt.to_period('M').astype(str)
df['dia_semana'] = df['fecha'].dt.day_name()

# Ventas por mes
ventas_mes = df.groupby('mes_ano')['total'].sum()

plt.figure(figsize=(10,5))
ventas_mes.plot(kind='line', marker='o')
plt.title('Ventas por mes')
plt.xlabel('Mes')
plt.ylabel('Total ventas')
plt.grid(True)
plt.tight_layout()
plt.show()

# Top 10 productos (barras)
top10 = df.groupby('producto')['cantidad'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,6))
top10.plot(kind='bar')
plt.title('Top 10 productos por cantidad vendida')
plt.xlabel('Producto')
plt.ylabel('Cantidad vendida')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Ventas por categoria (pastel)
ventas_cat = df.groupby('categoria')['total'].sum()
plt.figure(figsize=(6,6))
ventas_cat.plot(kind='pie', autopct='%1.1f%%')
plt.title('Porcentaje de ventas por categoría')
plt.ylabel('')
plt.tight_layout()
plt.show()
