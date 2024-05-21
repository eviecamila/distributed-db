
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
AND=' AND '

@app.route('/calls_d', methods=['GET'])
def llamadas_distribuidas():
    data = request.args
    try:
        src, dst, status, c, d1, d2, src, dst = [
            None, None, None, ["M", "N", "O"], None, None, None, None]

        src = data.get('s')

        dst = data.get('d')
        if data.get('c'):
            c = data.get('c').split(',')
        status = data.get('e')
        d1 = data.get('d1')
        d2 = data.get('d2')
        src = data.get('src')
        dst = data.get('dst')
        query = ''
        if c:
            for city in c:
                put_union = False
                sub_query = f"SELECT *, '{city}' AS branch FROM sucursal{sucursales[city]}.cdr"
                if src or dst or status or d1 or d2:
                    sub_query += " WHERE "
                    if src:
                        sub_query += f"src = '{src}'"
                        put_union = True
                    if dst:
                        if put_union: sub_query += AND
                        sub_query += f"dst = '{dst}'"
                        put_union = True
                    if status:
                        if put_union: sub_query += AND
                        sub_query += f"disposition = '{estados_llamada[status]}'"
                        put_union = True
                    
                    if d1 and d2:
                        if put_union: sub_query += AND
                        sub_query += f"calldate BETWEEN '{data['d1']}' AND '{data['d2']}'"
                        put_union = True
                    else:
                        if d1:
                            if put_union: sub_query += AND
                            sub_query += f"calldate >= '{data['d1']}'"
                            put_union = True
                        elif d2:
                            if put_union: sub_query += AND
                            sub_query += f"calldate <= '{data['d2']}'"
                            put_union = True
                    if src:
                        sub_query += f"src = '{src}'"
                        put_union = True
                    if dst:
                        if put_union: sub_query += AND
                        sub_query += f"dst = '{dst}'"
                        put_union = True
                if query:  query += " UNION ALL "
                query += sub_query
        print 

        ex = data.get('w') == '1'
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
                'sequence': row[25],
                'branch': row[26]
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
