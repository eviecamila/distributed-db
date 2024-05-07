from flask import Flask, jsonify

# Creamos una instancia de Flask
app = Flask(__name__)

# Definimos una ruta para el endpoint principal
@app.route('/')
def index():
    return "¡Hola! Esta es mi API."

# Definimos una ruta para un endpoint que devuelve datos JSON
@app.route('/api/ejemplo', methods=['GET'])
def ejemplo():
    datos = {
        'mensaje': 'Este es un ejemplo de datos JSON desde Flask.',
        'status': 'success'
    }
    return jsonify(datos)

if __name__ == '__main__':
    # Ejecutamos la aplicación en el puerto 5000
    app.run(debug=True)
