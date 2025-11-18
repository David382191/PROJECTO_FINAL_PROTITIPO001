import mysql.connector

# --------------------------------------------
# 1. CONECTARSE A LA BASE DE DATOS
# --------------------------------------------
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # <-- cámbialo si tienes otro usuario
        password="12345",          # <-- agrega tu contraseña si tienes
        database="chatbot_demo"
    )

# --------------------------------------------
# 2. GUARDAR DATOS DEL FORMULARIO
# --------------------------------------------
def guardar_formulario(nombre, edad):
    db = conectar_db()
    cursor = db.cursor()

    sql = "INSERT INTO formulario (nombre, edad) VALUES (%s, %s)"
    cursor.execute(sql, (nombre, edad))

    db.commit()
    cursor.close()
    db.close()

# --------------------------------------------
# 3. CHATBOT SIMPLE
# --------------------------------------------
def chatbot():
    print("Hola 👋, soy el chatbot de prueba.")
    print("Te haré unas preguntas básicas...\n")

    nombre = input("¿Cuál es tu nombre? ➤ ")
    edad = input("¿Cuál es tu edad? ➤ ")

    # Validar edad
    if not edad.isdigit():
        print("La edad debe ser un número. Intenta otra vez.")
        return

    # Guardar en MySQL
    guardar_formulario(nombre, int(edad))

    print("\n¡Gracias! 🙌 Tus datos han sido registrados correctamente.")
    print("Fin del prototipo.")

# --------------------------------------------
# 4. EJECUCIÓN
# --------------------------------------------
if __name__ == "__main__":
    chatbot()
