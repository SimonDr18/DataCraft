from .app import app
from flask import render_template
from .db import get_books, get_book, get_books_for_author

@app.route("/")
def home():
    return render_template(
    "home.html",
    title="Hello World!",
    data=get_books()
    )

@app.route("/book/<int:index>")
def book(index):
    return get_book(index)["title"]

@app.route("/book/<string:name>")
def author(name):
    return get_books_for_author(name)
