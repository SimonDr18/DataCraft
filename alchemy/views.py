from .app import app
from flask import render_template
from .models import *

@app.route("/")
def home():
    return render_template(
    "home.html",
    title="Hello World!",
    data=get_books()
    )

@app.route("/books")
def books():
    return render_template(
    "books.html",
    title="Les livres sur Amazon",
    data=get_books()
    )

@app.route("/authors")
def authors():
    return render_template(
    "authors.html",
    title="Les auteurs",
    data=get_authors()
    )

@app.route("/book/<int:index>")
def book(index):
    return get_book(index).title

@app.route("/book/<string:name>")
def author(name):
    return render_template(
    "books.html",
    title="Les livres de "+name,
    data=get_books_for_author(name)
    )
