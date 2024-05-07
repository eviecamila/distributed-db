
from yoshi.te.mete.gol.gog_gog import evie_troll
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
        data = {'src': None, 'dst': None, 'status': None, 'c': None}
        try:
            data['src'] = request.args['s']
        except:
            pass
        try:
            data['dst'] = request.args['d']
        except:
            pass
        try:
            data['c'] = request.args['c']
        except:
            pass
        try:
            data['status'] = request.args['status']
        except:
            pass

        # Construir la consulta SQL
        query = "SELECT * FROM cdr"
        put_where = False
        if data['src'] or data['dst'] or data['c'] or data['status']:
            query += " WHERE "
            if data['src']:
                query += f"src = '{data['src']}'"
                put_where = True
            if data['dst'] and put_where:
                query += " AND "
                query += f"dst = '{data['dst']}'"
            elif not put_where: put_where = True
            if data['c'] and put_where:
                query += " AND "
                query += f"branch = '{data['c']}'"
            elif not put_where: put_where = True
            if data['status'] and put_where:
                query += " AND "
                query += f"status = '{data['status']}'"
            elif not put_where: put_where = True

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


#Hash table para los cosos aquellos
sucursales = {"M":"Mochis","N":"Navojoa","O":"Obregon"}
estados_llamada = {"A":"ANSWERED","N":"NO ANSWER","B":"BUSY", "F":"FAILED"}

@app.route('/calls_d', methods=['GET'])
def llamadas_distribuidas():
    try:
        data = {'src': None, 'dst': None, 'status': None, 'c': ["M", "N", "O"]}
        try:
            data['src'] = request.args['s']
        except:
            pass
        try:
            data['dst'] = request.args['d']
        except:
            pass
        try:
            data['c'] = request.args['c'].split(',')
        except:
            pass
        try:
            data['status'] = request.args['e']
        except:
            pass
        print(data['c'])
        # Construir la consulta SQL
        query = ''
        if data['c']:
            for city in data['c']:
                put_union = False
                sub_query = f"SELECT *, '{city}' AS branch FROM sucursal{sucursales[city]}.cdr"
                if data['src'] or data['dst'] or data['status']:
                    sub_query += " WHERE "
                    if data['src']:
                        sub_query += f"src = '{data['src']}'"
                        put_union = True
                    if data['dst']:
                        if put_union:
                            sub_query += " AND "
                        sub_query += f"dst = '{data['dst']}'"
                        put_union = True
                    if data['status']:
                        if put_union:
                            sub_query += " AND "
                        sub_query += f"disposition = '{estados_llamada[data['status']]}'"
                        put_union = True
                if query:
                    query += " UNION ALL "
                query += sub_query

        ex = False
        try:
            ex = request.args['w'] == '1'
        except:
            pass
        print(f'{"S" if ex else "No s"}e guardará en resultados_cdr.csv')

        # print(query)
        # Obtener los resultados
        results = connection.select_query(query, ex)

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
        return jsonify([])  # Retorna una lista vacía en caso de error o si no se cumple ninguna condición

evie_troll()


if __name__ == '__main__':
    # Ejecutamos la aplicación en el puerto 5000
    app.run(debug=True)
