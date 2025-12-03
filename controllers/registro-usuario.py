from database.db import get_connection

conexion = get_connection()
cursor = conexion.cursor(dictionary=True)

cursor.execute("SELECT * FROM administrador_secretaria")
registros = cursor.fetchall()

for fila in registros:
    print(fila)

cursor.close()
conexion.close()
