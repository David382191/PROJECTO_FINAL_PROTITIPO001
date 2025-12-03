from flask import Flask, render_template, request
import mysql.connector
import ollama
from datetime import datetime

app = Flask(__name__)

# ---------------------------------------
#  CONEXIÓN A LA BD
# ---------------------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        port="3307",
        user="root",
        password="12345",
        database="chatbot_secretaria"
    )

# ---------------------------------------
#  OBTENER O CREAR CONVERSACIÓN
# ---------------------------------------
def obtener_conversacion():
    conn = get_db()
    cursor = conn.cursor()

    # Ver si hay alguna conversación en curso
    cursor.execute("SELECT ID_CONVERSACION FROM CONVERSACION ORDER BY ID_CONVERSACION DESC LIMIT 1")
    fila = cursor.fetchone()

    if fila:
        id_conv = fila[0]
    else:
        # Crear una nueva conversación
        cursor.execute("""
            INSERT INTO CONVERSACION (Usuario, Fecha_hora)
            VALUES (%s, %s)
        """, ("usuario_principal", datetime.now()))
        conn.commit()
        id_conv = cursor.lastrowid

    cursor.close()
    conn.close()
    return id_conv

# ---------------------------------------
#  GUARDAR MENSAJE EN LA BD
# ---------------------------------------
def guardar_mensaje(id_conversacion, remitente, contenido):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO MENSAJE (ID_CONVERSACION, Remitente, Contenido, Fecha_hora)
        VALUES (%s, %s, %s, %s)
    """, (id_conversacion, remitente, contenido, datetime.now()))

    conn.commit()
    cursor.close()
    conn.close()

# ---------------------------------------
#  PALABRAS CLAVE
# ---------------------------------------
def buscar_palabra_clave(texto_usuario):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT Respuesta_designada 
        FROM PALABRA_CLAVE 
        WHERE %s LIKE CONCAT('%', Palabra, '%');
    """

    cursor.execute(query, (texto_usuario,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        return resultado["Respuesta_designada"]
    
    return None

# ---------------------------------------
#  RESPUESTA IA (OLLAMA)
# ---------------------------------------
def responder_con_llama(texto):
    respuesta = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": texto}]
    )
    return respuesta["message"]["content"]

# ---------------------------------------
#  RUTA PRINCIPAL
# ---------------------------------------
@app.route("/", methods=["GET", "POST"])
def chat():
    respuesta = None
    texto_usuario = ""

    if request.method == "POST":
        texto_usuario = request.form["mensaje"]
        id_conv = obtener_conversacion()

        # Guardar mensaje del usuario
        guardar_mensaje(id_conv, "usuario", texto_usuario)

        # Respuesta: palabra clave o IA
        respuesta = buscar_palabra_clave(texto_usuario)
        if not respuesta:
            respuesta = responder_con_llama(texto_usuario)

        # Guardar respuesta del bot
        guardar_mensaje(id_conv, "bot", respuesta)

    return render_template("chat.html", respuesta=respuesta, mensaje=texto_usuario)

if __name__ == "__main__":
    app.run(debug=True)
