import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

#se carga y prepara
conn = sqlite3.connect('mama_coneja.db')
df = pd.read_sql_query("SELECT v.*, p.nombre as producto, p.precio, cat.nombre as categoria FROM ventas v JOIN productos p ON v.producto_id=p.id JOIN categorias cat ON p.categoria_id=cat.id", conn, parse_dates=['fecha'])
conn.close()

#Factura simple
df['mes'] = df['fecha'].dt.month
df['dia'] = df['fecha'].dt.day
df['dia_semana'] = df['fecha'].dt.dayofweek  
#por categoria
df = pd.get_dummies(df, columns=['categoria'], drop_first=True)

#se suman ventas por dia
daily = df.groupby(df['fecha'].dt.date).agg({
    'total':'sum',
    'mes':'first',
    'dia':'first',
    'dia_semana':'first',
    **{col: ('first' if col.startswith('categoria_') else 'first') for col in df.columns if col.startswith('categoria_')}
}).reset_index()

#Definicion de variables
X = daily.drop(columns=['fecha','total'])
y = daily['total']

#cuadro
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, pred))
print("RMSE:", rmse)

#Se mustran datos
res = pd.DataFrame({'real': y_test.values, 'pred': pred})
print(res.head())
