from flask import Flask
import pandas as pd

app = Flask(__name__)

@app.route("/")
def inicio():

    data = pd.read_csv("../dataset/consumo_energetico.csv")

    return data.to_json()

app.run(debug=True)
