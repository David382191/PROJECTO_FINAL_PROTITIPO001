from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_super_secreta_123"

# Conexión a la BD
conexion = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="12345",
    database="base_ejemplo_prueba"
)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["username"]
        password = request.form["password"]

        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users a WHERE username=%s AND password=%s",
                       (usuario, password))
        admin = cursor.fetchone()

        if admin:
            session["admin_id"] = admin["id"]
            return redirect("/panel")
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")


@app.route("/panel")
def panel():
    if "admin_id" not in session:
        return redirect("/")

    return render_template("panel.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
