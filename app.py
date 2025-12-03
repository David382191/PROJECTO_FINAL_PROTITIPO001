from flask import Flask, render_template, request
import mysql.connector
import ollama

app = Flask(__name__)

# -----------------------------
# CONEXIÓN A LA BD
# -----------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        port="3307",
        user="root",
        password="12345",
        database="chatbot_secretaria"
    )

# -----------------------------
# PALABRA CLAVE
# -----------------------------
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

# -----------------------------
# IA CON LLAMA
# -----------------------------
def responder_con_llama(texto):
    respuesta = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": texto}]
    )
    return respuesta["message"]["content"]

# -----------------------------
# RUTA PRINCIPAL
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def chat():
    respuesta = None
    texto_usuario = ""

    if request.method == "POST":
        texto_usuario = request.form["mensaje"]

        # Intentar palabra clave
        respuesta = buscar_palabra_clave(texto_usuario)

        # Si no existe, usar IA
        if not respuesta:
            respuesta = responder_con_llama(texto_usuario)

    return render_template("chat.html", respuesta=respuesta, mensaje=texto_usuario)


if __name__ == "__main__":
    app.run(debug=True)
