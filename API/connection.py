import mysql.connector

# Configuración de la conexión
config = {
  'user': 'evie',
  'password': 'evie',
  'host': '192.168.183.190',
  'database': 'asteriskcdrdb',
  'raise_on_warnings': True
}

def connect():
        # Establecer la conexión
    try:
        conn = mysql.connector.connect(**config)
        print("Conexión exitosa a la base de datos")
        
        # Ejecutar una consulta
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cdr")
        
        # Obtener los resultados
        for row in cursor.fetchall():
            print(row)
        
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print("Error de conexión a la base de datos:", err)


connect()