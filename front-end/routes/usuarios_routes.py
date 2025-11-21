from flask import Blueprint, render_template, redirect, session

registrousuario_bp = Blueprint("registro-usuario_bp", __name__)
###
@registrousuario_bp.route("/registro-usuario")
def home():
    if "admin_id" not in session:
        return redirect("/")
    return render_template("registro-usuario.html")