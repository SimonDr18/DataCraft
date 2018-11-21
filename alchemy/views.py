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

# @app.route("/books")
# def books():
#     return render_template(
#     "books.html",
#     title="Les livres sur Amazon",
#     data=get_books()
#     )
#
# @app.route("/author")
# def author():
#     pass
#
# @app.route("/book/<int:index>")
# def book(index):
#     return get_book(index)["title"]
#
# @app.route("/book/<string:name>")
# def author(name):
#     return get_books_for_author(name)
