import pandas as pd
import sqlite3
#Coneccion a sql
conn = sqlite3.connect('mama_coneja.db')

query = """
SELECT 
    v.id,
    v.fecha,
    v.producto_id,
    v.cliente_id,
    v.cantidad,
    v.total,
    p.nombre AS producto,
    p.precio,
    cat.nombre AS categoria
FROM ventas v
JOIN productos p ON v.producto_id = p.id
JOIN categorias cat ON p.categoria_id = cat.id;
"""

df = pd.read_sql_query(query, conn)
conn.close()

print("Columnas cargadas desde SQLite:")
print(df.columns)

#Conversion de fechas o dias de la semana
df['fecha'] = pd.to_datetime(df['fecha'])

df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month
df['dia_semana'] = df['fecha'].dt.day_name()

#Definicion de ventas por mes 

ventas_mes = df.groupby(['año', 'mes']).agg({'total': 'sum'}).reset_index()
print("\n📌 Ventas por mes:")
print(ventas_mes)

#Ventas por categorias
ventas_cat = (
    df.groupby('categoria')
    .agg({'total': 'sum', 'cantidad': 'sum'})
    .sort_values('total', ascending=False)
    .reset_index()
)

print("Ventas por categoria:")
print(ventas_cat)

#Ventas ala semana
orden_dias = ['Lunes', 'Martes', 'Miercoles', 'Vueves', 'Viernes', 'Sabado', 'Domingo']

ventas_d_sem = (
    df.groupby('dia_semana')
    .agg({'total': 'sum'})
    .reindex(orden_dias)
)

print("Ventas por dia de la semana:")
print(ventas_d_sem)
