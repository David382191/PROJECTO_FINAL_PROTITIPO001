## Por Alfonso Espinoza
from flask import Blueprint, render_template, session, redirect

panel = Blueprint("panel", __name__)

@panel.route("/home")
def home():
    if "admin_id" not in session:
        return redirect("/")
    return render_template("home.html")