from flask import render_template, redirect, request, session, flash, abort
from app import app
from db import db
import user
import forum
import secrets
import thread


def error(message, destination):
    flash(message)
    return redirect(destination)

@app.route("/")
def index():
    forums = forum.get_all()
    return render_template("index.html", forums = forums)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    confirm = request.form.get("confirm", "").strip()

    if not username or not 3 <= len(username):
        return error("Käyttäjätunnus on liian lyhyt", request.path)
    if not password or not 8 <= len(password):
        return error("Salasanan tulee olla ainakin kahdeksan merkkiä pitkä", request.path)
    if password != confirm:
        return error("Salasanat eivät täsmää", request.path)
    if user.user_exists(username):
        return error("Käyttäjätunnus on jo olemassa", request.path)
    user.register(username, password)
    account = user.get(username)
    session["username"] = username
    session["admin"] = False
    session["id"] = account[0]
    session["csrf_token"] = secrets.token_hex(16)
    session["allowed"] = user.get_allowed_forums(account[0])
    return redirect("/")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username", "")
    if not username.strip() or not user.user_exists(username):
        return error("Väärä käyttäjänimi", request.path)
    password = request.form.get("password", "")
    if not password.strip():
        return error("Väärä salasana", request.path)
    account = user.check_password(username, password)
    if account is None:
        return error("Väärä salasana", request.path)
    else:
        session["id"] = account[0]
        session["admin"] = account[1]
        session["username"] = account[2]
        session["csrf_token"] = secrets.token_hex(16)
        session["allowed"] = user.get_allowed_forums(account[0])
    return redirect("/")
    
@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("admin", None)
    session.pop("id", None)
    session.pop("csrf_token", None)
    session.pop("allowed", None)
    return redirect("/")

@app.route("/promote/")
def promote():
    user_id = session.get("id")
    if user_id:
        user.promote(user_id)
        session["admin"] = True
    return redirect("/")

@app.route("/demote/")
def demote():
    user_id = session.get("id")
    if user_id:
        user.demote(user_id)
        session["admin"] = False
    return redirect("/")

@app.route("/forums/<int:id>")
def render_forum(id):
    exists = forum.exists(id)
    edit = request.args.get("edit") == "1"
    if exists:
        threads = thread.get_all(id)
        found_forum = forum.get(id)
        if found_forum[1] and not session.get("admin") and found_forum[0] not in session.get("allowed", []):
            return render_template("norights.html")
        return render_template("forum.html", forum=found_forum, threads=threads, edit=edit)
    else:
        return redirect("/")

@app.route("/createthread", methods=["POST"])
def create_thread():
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
    if session.get("id"):
        title = request.form.get("title")
        forum_id = request.form.get("forum_id")
        if len(title) > 50:
            return error("Otsikko ei saa olla yli 50 merkkiä pitkä", f"/forums/{forum_id}")
        if not thread.create(title, forum_id, session["id"]):
            flash("Langan otsikko ei voi olla tyhjä.") 
    return redirect(f"/forums/{forum_id}")

@app.route("/deletethread", methods=["POST"])
def delete_thread():
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
    thread_id = request.form.get("thread_id")
    forum_id = request.form.get("forum_id")
    if thread_id:
        thread.delete(forum_id, thread_id, session.get("admin"), session.get("id"))
    return redirect(f"/forums/{forum_id}?edit=1")

@app.route("/createforum", methods=["POST"])
def create_forum():
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
    if session.get("admin"):
        topic = request.form.get("topic")
        hidden = request.form.get("hidden")
    if len(topic) > 50:
            return error("Ärsytyksenaihe ei saa olla yli 50 merkkiä pitkä", "/")
    if not forum.create(topic, bool(hidden)):
        flash("Aiheen nimi ei voi olla tyhjä.")       
    return redirect("/")

@app.route("/deleteforum", methods=["POST"])
def delete_forum():
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
    if session.get("admin"):
        forum_id = request.form.get("forum_id")
        forum.delete(forum_id)
    return redirect("/")