from .app import app
from flask import render_template
from .db import get_books, get_book, get_books_for_author
from .models import get_sample

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

# @app.route("/author")
# def author():
#     return render_template(
#     "author.html",
#     title="Les auteurs",
#     data=get_books()
#     )

@app.route("/book/<int:index>")
def book(index):
    return get_book(index)["title"]

@app.route("/book/<string:name>")
def author(name):
    return get_books_for_author(name)
