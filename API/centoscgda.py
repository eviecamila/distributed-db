# -*- coding: utf-8 -*-
import csv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import pymysql.cursors  # Necesitas instalar pymysql, por ejemplo, con "pip install pymysql"

# Conexión a la base de datos MySQL
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='tu_contraseña',
                             database='tu_base_de_datos',
                             cursorclass=pymysql.cursors.DictCursor)

# Método para ejecutar la consulta SQL y guardar los resultados en un archivo CSV
def select_query_with_branch(query="SELECT src, dst, d1, d2, status, 'M' AS branch FROM sucursalMochis.cdr UNION ALL SELECT src, dst, d1, d2, status, 'N' AS branch FROM sucursalNavojoa.cdr UNION ALL SELECT src, dst, d1, d2, status, 'O' AS branch FROM sucursalObregon.cdr"):
    try:
        print("Ejecutando '{}'".format(query))

        # Comando para ejecutar la consulta SQL y guardar los resultados en un archivo CSV
        command = "mysql -u root -e \"{}\" > resultados_cdr.csv".format(query)

        # Ejecutar el comando en la terminal
        os.system(command)

        print("Consulta ejecutada con éxito. Resultados guardados en resultados_cdr.csv")
        return 'XD'
    except Exception as e:
        print("Error al ejecutar la consulta:", e)

# Método para leer el archivo CSV y convertir los datos a formato JSON
def read_csv_to_json(csv_file):
    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            return json.dumps(data)
    except Exception as e:
        print("Error al leer el archivo CSV:", e)
        return None

# Define el manejador de solicitudes personalizado
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # Método para manejar las solicitudes GET
    def do_GET(self):
        # Establece el código de estado de la respuesta
        self.send_response(200)
        # Establece las cabeceras de la respuesta
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # Envía el cuerpo de la respuesta
        json_data = select_query_with_branch()
        if json_data:
            self.wfile.write(json_data.encode())
        else:
            self.wfile.write(b"No se pudo generar el JSON.")

# Crea una instancia del servidor HTTP con el manejador de solicitudes personalizado
# Escucha en todas las interfaces en el puerto 8000
server_address = ('127.0.0.1', 8000)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

# Inicia el servidor y espera indefinidamente por solicitudes entrantes
print('Starting server...')
httpd.serve_forever()
