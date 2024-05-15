import pymysql.cursors

# Configuración de la conexión a la base de datos
config = {
    "host": "0.tcp.us-cal-1.ngrok.io",
    "user": "admindb",
    "password": "admin",
    "database": "sucursalMochis",
    "port": 13386,
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}


def select_query_with_branch(query="SELECT calldate,src,dst,duration,disposition,ciudad FROM VSucursales"):
    try:
        print("Ejecutando '{}'".format(query))
        
        # Establecer conexión a la base de datos
        connection = pymysql.connect(host='localhost',
                             user='evie',
                             password='evie',
                             database='sucursalMochis',
                             cursorclass=pymysql.cursors.DictCursor)
        
        with connection:
            # Crear un cursor
            with connection.cursor() as cursor:
                # Ejecutar la consulta
                cursor.execute(query)
                # Obtener los resultados
                results = cursor.fetchall()
                
                # Convertir objetos datetime a cadena
                for row in results:
                    for key, value in row.items():
                        if isinstance(value, datetime):
                            row[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                
                # Convertir los resultados a formato JSON
                return json.dumps(results)
    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        return None


def filtrado(params):
    try:
        # Establecer conexión a la base de datos
        connection = pymysql.connect(**config)

        # Definir la consulta SQL con parámetros
        query = "CALL Filtrar(%s, %s, %s, %s, %s, %s);"

        # Ejecutar la consulta con los parámetros proporcionados
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    params["src"],
                    params["dst"],
                    params["d1"],
                    params["d2"],
                    params["status"],
                    params["city"],
                ),
            )

            # Obtener los resultados de la consulta
            data = cursor.fetchall()

        return data

    except pymysql.MySQLError as e:
        print("Error de conexión a la base de datos:", e)

    finally:
        # Cerrar la conexión a la base de datos
        if connection:
            connection.close()


# Ejemplo de uso de la función filtrado con parámetros
# params = {"src": "valor1", "dst": "valor2", "d1": "valor3", "d2": "valor4", "status": "valor5", "city": "valor6"}
# results = filtrado(params)
# print(results)
