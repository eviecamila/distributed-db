from flask import Flask, jsonify, request
from flask_cors import CORS
import connection

# Creamos una instancia de Flask
app = Flask(__name__)

# Definimos una ruta para el endpoint principal


@app.route("/")
def index():
    return "¡Hola! Esta es mi API."


# Definimos una ruta para un endpoint que devuelve datos JSON


@app.route("/api/ejemplo", methods=["GET"])
def ejemplo():
    datos = connection.select_query_with_branch()
    return jsonify(datos)



@app.route("/calls_d", methods=["POST"])
def llamadas_distribuidas():
    data = request.json
    try:
        results = connection.filtrado(data)
        return jsonify(results)
    except Exception as e:
        print("Error:", e)
        # Retorna una lista vacía en caso de error o si no se cumple ninguna condición
        return jsonify(e)


CORS(app)
if __name__ == "__main__":
    # Ejecutamos la aplicación en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=8000)
