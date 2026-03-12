from flask import Flask, render_template
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Cargar datos
data = pd.read_csv("../dataset/consumo_energetico.csv")

# Estadísticas
consumo_promedio = round(data["consumo_kwh"].mean(),2)
consumo_max = data["consumo_kwh"].max()
consumo_min = data["consumo_kwh"].min()

# Modelo IA
X = np.array(range(len(data))).reshape(-1,1)
y = data["consumo_kwh"]

modelo = LinearRegression()
modelo.fit(X,y)

prediccion = round(modelo.predict([[12]])[0],2)

# Alertas
limite = 160
alertas = []

for consumo in data["consumo_kwh"]:
    if consumo > limite:
        alertas.append(consumo)

@app.route("/")
def index():
    
    return render_template(
        "index.html",
        promedio=consumo_promedio,
        maximo=consumo_max,
        minimo=consumo_min,
        prediccion=prediccion,
        alertas=alertas
    )

if __name__ == "__main__":
    app.run(debug=True)
