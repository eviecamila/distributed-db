
from flask import Flask, jsonify, request
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


@app.route('/calls', methods=['GET'])
def llamadas():
    try:
        data = {'src':None, 'dst':None, 'status':None}
        try:data['src'] = request.args['s']
        except: pass
        try:data['dst'] = request.args['d']
        except: pass
        try:data['status'] = request.args['status']
        except: pass
        
        # Construir la consulta SQL
        query = f"SELECT * FROM cdr"
        # Construir la consulta SQL
        query = "SELECT * FROM cdr"
        put_where = False
        if data['src'] or data['dst'] or data['status']:
            query += " WHERE "
            if data['src']:
                query += f"src = '{data['src']}'"
                put_where = True
            if data['dst']:
                if put_where:
                    query += " AND "
                query += f"dst = '{data['dst']}'"
                put_where = True
            if data['status']:
                if put_where:
                    query += " AND "
                query += f"status = '{data['status']}'"
                put_where = True
        # Completar query si existen los datos:

        # Obtener los resultados
        results = connection.select_query(query)
        
        # Convertir los resultados a un formato JSON
        json_data = []
        for row in results:
            json_data.append({
                'calldate': row[0],
                'clid': row[1],
                'src': row[2],
                'dst': row[3],
                'dcontext': row[4],
                'channel': row[5],
                'dstchannel': row[6],
                'lastapp': row[7],
                'lastdata': row[8],
                'duration': row[9],
                'billsec': row[10],
                'disposition': row[11],
                'amaflags': row[12],
                'accountcode': row[13],
                'uniqueid': row[14],
                'userfield': row[15],
                'did': row[16],
                'recordingfile': row[17],
                'cnum': row[18],
                'cnam': row[19],
                'outbound_cnum': row[20],
                'outbound_cnam': row[21],
                'dst_cnam': row[22],
                'linkedid': row[23],
                'peeraccount': row[24],
                'sequence': row[25]
            })

        return jsonify(json_data)

    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    # Ejecutamos la aplicación en el puerto 5000
    app.run(debug=True)
