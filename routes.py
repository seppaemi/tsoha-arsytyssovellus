from flask import render_template, redirect, request, session, flash, abort
from app import app
from db import db
import user
import forum


@app.route("/")
def index():
    forums = forum.get_all()
    return render_template("index.html", forums = forums)