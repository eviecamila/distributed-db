
from yoshi.te.mete.gol.gog_gog import evie_troll
from flask import Flask, jsonify, request
from flask_cors import CORS
import connection
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


# Hash table para los cosos aquellos
sucursales = {"M": "Mochis", "N": "Navojoa", "O": "Obregon"}
estados_llamada = {
    "A": "ANSWERED",
    "N": "NO ANSWER",
    "B": "BUSY", "F":
    "FAILED"
}
AND = ' AND '


@app.route('/calls_d', methods=['GET'])
def llamadas_distribuidas():
    data = request.args
    try:
        src, dst, status, c, d1, d2 = [
            data.get('src') or None, data.get('dst') or None,
            data.get('e') or None, data.get('c') or None,
            data.get('d1') or None, data.get('d2') or None]

        query = 'SELECT * FROM ViewSucursales'
        # Add Where
        if src or dst or status or c or d1 or d2:
            query += ' WHERE '

        if src:  # Origen
            query += f'src = "{src}"'
            if dst or d1 or d2 or status or c:
                query += AND
        if dst:  # Destino
            query += f'dst = "{dst}"'
            if d1 or d2 or status or c:
                query += AND
        if d1 and d2:  # Fechas inicio  y Fin
            query += f'calldate BETWEEN "{d1}" AND "{d2}"'
            if status or c:
                query += AND
        elif d1:
            query += f'calldate >= "{d1}"'
            if status or c:
                query += AND
        elif d2:
            query += f'calldate <= "{d2}"'
            if status or c:
                query += AND
        if status:  # Estado de llamada
            query += f'disposition = "{estados_llamada[status]}"'
            if c:
                query += AND
        if c:
            query += f'branch = "{c}"'  # Ciudad

        # query += sub_query

        ex = data.get('w') == '1'
        print(f'{"S" if ex else "No s"}e guardará en resultados_cdr.csv')

        # print(query)
        # Obtener los resultados
        results = connection.select_query(query, {
            'src': src,
            'dst': dst,
            'd1': d1,
            'd2': d2,
            'disposition': status,
            'city': None,  # Asegúrate de reemplazar esto con el valor adecuado si se utiliza
        })

        # Convertir los resultados a un formato JSON
        json_data = []
        for row in results:
            json_data.append({
                'calldate': row[0],
                'src': row[1],
                'dst': row[2],
                'billsec': row[3],
                'disposition': row[4],
                'branch': row[5]
            })
        return jsonify(json_data)
    except Exception as e:
        print("Error:", e)
        # Retorna una lista vacía en caso de error o si no se cumple ninguna condición
        return jsonify([])


evie_troll()

CORS(app)
if __name__ == '__main__':
    # Ejecutamos la aplicación en el puerto 5000
    app.run(debug=True)
