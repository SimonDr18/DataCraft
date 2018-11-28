from .app import app
from flask import render_template
from .models import *
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms.validators import DataRequired

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

@app.route("/author/<int:id>")
def author(id):
    a=get_author(id)
    return render_template(
    "books.html",
    title="Les livres de "+a.name,
    data=get_books_for_author(a.name)
    )

class AuthorForm(FlaskForm):
    id=HiddenField('id')
    name = StringField('Nom', validators=[DataRequired()])

@app.route("/edit/author/<int:id>")
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id = a.id, name=a.name)
    return render_template(
    "edit-author.html",
    author=a, form=f
    )

from flask import url_for, redirect
from .app import db

@app.route("/save/author", methods=("POST",))
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = get_author(id)
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for('author',id=a.id))
    a = get_author(int(f.id.data))
    return render_template(
    "edit-author.html",
    author=a, form=f)

@app.route("/add/author/")
def add_author():
    f = AuthorForm()
    return render_template(
    "add_author.html",
    form=f
    )

@app.route("/create/author",methods=("POST",))
def add_author_POST():
    n=None
    f=AuthorForm()
    if f.validate_on_submit():
        n = Author(name = f.name.data)
        db.session.add(n)
        db.session.commit()
        return redirect(url_for("author",id=n.id))
    return render_template(
    "add_author.html",
    form = f
    )
