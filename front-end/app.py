## Alfonso Espinoza.
###########################################################################################
##Aquí primero vamos a traer las librerías que usaremos aquí.
from flask import Flask, render_template, request, redirect, session
import mysql.connector ##esto de acá esuna libreria...negro

from database.db import get_connection   # <<--- IMPORTAMOS LA BD
###########################################################################################
# CREAR APP DE FLASK
app = Flask(__name__)
#Esta es una contraseña que usaremos más tarde. 
app.secret_key = "clave_super_secreta_123"
###########################################################################################
###########################################################################################
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["username"]
        password = request.form["password"]

        #Aquí vamos a necesitar usar consultas SQL, por lo que
        # necesitamremos abrir un lugar donde ejecutarlas,
        # eso lo que hace esto de aquí abajo. 
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        #de esta forma podemos hacer consultas a la base de datos SQL como esta.
        #Los %s evitan SQL Injection. Mientras que se leeran los valores que enviamos.
        cursor.execute("SELECT * FROM administrador_secretaria a WHERE usuario=%s AND contrasena=%s",
                       (usuario, password))
        
        admin = cursor.fetchone()
        cursor.close()
        conexion.close()

        ##Aquí es donde funciona el redirecionamiento.
        if admin:
            session["admin_id"] = admin["idAdmin"]
            ##Si todo está bien, nos enviará a este lugar. Aquí es donde podemos cambiarlo.
            return redirect("/home")
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")
###########################################################################################
###########################################################################################
@app.route("/home")
def home():
    if "admin_id" not in session:
        return redirect("/")
    return render_template("home.html")
###########################################################################################
###########################################################################################
@app.route("/panel")
def panel():
    if "admin_id" not in session:
        return redirect("/")
    return render_template("panel.html")
###########################################################################################
###########################################################################################
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
###########################################################################################
###########################################################################################
if __name__ == "__main__":
    app.run(debug=True)
###########################################################################################
###########################################################################################
##Listo, Roberto, terminamos aquí.