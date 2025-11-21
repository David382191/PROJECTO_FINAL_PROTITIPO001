#### Aquí vamos a poner esta vaina de la base de datos.
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="12345",
        database="chatbot_turnos"
    )