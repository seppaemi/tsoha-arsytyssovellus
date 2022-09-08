from app import app
from flask import render_template, request, redirect, make_response
import users
from db import db

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) == 0 or len(password) == 0:
            return render_template("login.html", error1="Virheellinen Käyttäjätunnus tai salasana")
        elif users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", error1="Virheellinen käyttäjätunnus tai salasana")
    
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if len(username) == 0 and len(password1) == 0:
            return render_template("register.html", error2="Anna käyttäjätunnus", error3="Anna salasana")
        if len(username) == 0:
            return render_template("register.html", error2="Anna käyttäjätunnus")
        if len(password1) == 0:
            return render_template("register.html", error3="Anna salasana")
        if password1 != password2:
            return render_template("register.html", error1="Salasanojen tulee olla samat")
        
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("register.html", error4=f"Käyttäjänimi {username} on varattu.")