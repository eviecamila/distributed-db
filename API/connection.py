import mysql.connector
# import csv


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

config = {
  'user': 'evie',
  'password': 'evie',
  'host': '192.168.183.190',
  'database': 'asteriskcdrdb',
  'raise_on_warnings': True
}

def select_query(query="SELECT * FROM cdr"):
    try:
        conn = mysql.connector.connect(**config)
        print("Conexión exitosa a la base de datos")
        print(f"Ejecutando '{query}'")
        
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        # Crear un archivo CSV y escribir los resultados
        # with open('resultados_cdr.csv', 'w', newline='') as csvfile:
            # csvwriter = csv.writer(csvfile)
            
            # Escribir el encabezado del CSV
            # csvwriter.writerow([i[0] for i in cursor.description])
            
            # Escribir los datos de la consulta al CSV
            # csvwriter.writerows(cursor)
        
        # print("Los resultados se han guardado en 'resultados_cdr.csv'")
        
        cursor.close()
        conn.close()
        return data

    except mysql.connector.Error as err:
        print("Error de conexión a la base de datos:", err)

# connect_and_write_to_csv()
