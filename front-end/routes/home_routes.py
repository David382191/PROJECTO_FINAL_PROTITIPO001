from flask import Blueprint, render_template, redirect, session

home_bp = Blueprint("home_bp", __name__)
###
@home_bp.route("/home")
def home():
    if "admin_id" not in session:
        return redirect("/")
    return render_template("home.html")