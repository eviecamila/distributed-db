@ -0,0 +1,99 @@
# -*- coding: utf-8 -*-
import csv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import os


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

# Define el manejador de solicitudes personalizado


def read_csv_to_json(csv_file):
    try:
        with open(csv_file, 'r') as file:
            # Utilizamos el dialecto 'excel' para manejar comillas y escapado de manera automática
            reader = csv.DictReader(file, dialect='excel')
            # Inicializamos una lista vacía para almacenar los datos
            data = []
            # Iteramos sobre cada fila del CSV
            for row in reader:
                # Creamos un diccionario para cada fila del CSV
                row_data = {
                    "src": row["src"],
                    "dst": row["dst"],
                    "d1": row["d1"],
                    "d2": row["d2"],
                    "status": row["status"],
                    "branch": row["branch"]
                }
                # Agregamos el diccionario a la lista de datos
                data.append(row_data)
            # Convertimos la lista de datos a formato JSON y la devolvemos
            return json.dumps(data)
    except Exception as e:
        print("Error al leer el archivo CSV:", e)
        return None


# Llamar a la función con el nombre del archivo CSV generado
json_data = read_csv_to_json('resultados_cdr.csv')
if json_data:
    print(json_data)
else:
    print("No se pudo generar el JSON.")


# Llamar a la función con el nombre del archivo CSV generado
json_data = read_csv_to_json('resultados_cdr.csv')
if json_data:
    print(json_data)
else:
    print("No se pudo generar el JSON.")


# Llamar a la función con el nombre del archivo CSV generado
json_data = read_csv_to_json('resultados_cdr.csv')
if json_data:
    print(json_data)
else:
    print("No se pudo generar el JSON.")


# Define el manejador de solicitudes personalizado

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # Método para manejar las solicitudes GET
    def do_GET(self):
        # Establece el código de estado de la respuesta
        self.send_response(200)
        # Establece las cabeceras de la respuesta
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Envía el cuerpo de la respuesta
        self.wfile.write(select_query_with_branch())


# Crea una instancia del servidor HTTP con el manejador de solicitudes personalizado
# Escucha en todas las interfaces en el puerto 8000
server_address = ('127.0.0.1', 8000)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

# Inicia el servidor y espera indefinidamente por solicitudes entrantes
print('Starting server...')
httpd.serve_forever()