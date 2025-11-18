
import mysql.connector

# --- Conexión a MySQL ---
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="secretaria"
    )

# --- Buscar horario en la BD ---
def obtener_horario(tramite):
    db = conectar()
    cursor = db.cursor()

    query = "SELECT horario FROM horarios WHERE nombre_tramite = %s"
    cursor.execute(query, (tramite,))
    resultado = cursor.fetchone()

    cursor.close()
    db.close()

    if resultado:
        return resultado[0]
    else:
        return None

# --- Chatbot muy básico ---
def chatbot():
    print("ChatBot: Hola, soy el asistente de Secretaría. ¿Qué trámite deseas consultar?")
    print("Opciones: matrículas, certificados, pagos")

    while True:
        mensaje = input("Tú: ").lower()

        if mensaje == "salir":
            print("ChatBot: ¡Hasta luego!")
            break

        horario = obtener_horario(mensaje)

        if horario:
            print(f"ChatBot: El horario para {mensaje} es: {horario}")
        else:
            print("ChatBot: No encontré información sobre ese trámite. Intenta con: matrículas, certificados o pagos.")

