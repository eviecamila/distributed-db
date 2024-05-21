import pymysql
import csv

# TODO: CAMBIAR DATOS DE ACCESO A LA DB en CENTOS

"""
# evie mamadisima
# Script para instalar la API cagada
yum install git
git clone https://github.com/eviecamila/distributed-db.git
cd API
pip install -r requirements.txt
py main.py
"""

# config = {
#     'user': 'admindb',
#     'password': 'admin',
#     'host': '0.tcp.us-cal-1.ngrok.io',
#     'database': 'sucursalMochis',
#     'port': '16567',
#     'raise_on_warnings': True
# }
config = {
    'user': 'admindb',
    'password': 'admin',
    'host': 'localhost',
    'database': 'sucursalMochis',
    'port': 3306,
}


def select_query_with_branch(query="SELECT *, 'M' AS branch FROM sucursalMochis.cdr UNION ALL SELECT *, 'N' AS branch FROM sucursalNavojoa.cdr UNION ALL SELECT *, 'O' AS branch FROM sucursalObregon.cdr"):
    try:
        conn = pymysql.connect(**config)
        print("Conexión exitosa a la base de datos")
        print(f"Ejecutando '{query}'")

        cursor = conn.cursor()
        cursor.execute(query)

        # Obtener los datos
        data = cursor.fetchall()

        # Obtener los nombres de las columnas
        column_names = [i[0] for i in cursor.description]

        # Escribir los resultados en el archivo CSV
        with open('resultados_cdr.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Escribir el encabezado del CSV
            csvwriter.writerow(column_names)
            # Escribir los datos de la consulta al CSV
            csvwriter.writerows(data)

        cursor.close()
        conn.close()
        return data

    except pymysql.MySQLError as err:
        print("Error de conexión a la base de datos:", err)


def select_query(query="SELECT * FROM cdr", write_csv=False):
    try:
        conn = pymysql.connect(**config)
        print("Conexión exitosa a la base de datos")
        print(f"Ejecutando '{query}'")

        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        if write_csv:
            with open('resultados_cdr.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                # Escribir el encabezado del CSV
                csvwriter.writerow(column_names)
                # Escribir los datos de la consulta al CSV
                csvwriter.writerows(data)
        cursor.close()
        conn.close()
        return data

    except pymysql.MySQLError as err:
        print("Error de conexión a la base de datos:", err)
