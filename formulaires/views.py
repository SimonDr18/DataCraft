from .app import app
from flask import render_template
from .models import *
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField, SelectField
from wtforms.validators import DataRequired
from flask import url_for, redirect, request
from .app import db
from hashlib import sha256
from flask_login import login_user, current_user, logout_user, login_required

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
    b = get_book(index)
    return render_template(
    "book.html",
    title="Le livre de "+b.title,
    data=b,
    login=current_user.is_authenticated
    )

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

class BookForm(FlaskForm):
    la = []
    listAuthor = get_authors()
    for a in listAuthor:
        la.append((a.id,a.name))
    id = HiddenField('id')
    title = StringField('Titre', validators=[DataRequired()])
    price = StringField('Prix', validators=[DataRequired()])
    url = StringField('URL du livre', validators=[DataRequired()])
    img = StringField('IMG du livre', validators=[DataRequired()])
    author = SelectField('Auteur', choices=la, validators=[DataRequired()])

@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id = a.id, name=a.name)
    return render_template(
    "edit-author.html",
    author=a, form=f
    )

@app.route("/save/author", methods=("POST",))
@login_required
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

@app.route("/add/author")
@login_required
def add_author():
    f = AuthorForm()
    return render_template(
    "add_author.html",
    form=f
    )

@app.route("/add/book")
@login_required
def add_book():
    f=BookForm()
    return render_template(
    "add_book.html",
    form = f
    )

@app.route("/create/author",methods=("POST",))
@login_required
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

@app.route("/create/book",methods=("POST",))
def add_book_POST():
    n=None
    f=BookForm()
    if f.validate_on_submit():
        a = get_author(f.author.data)
        n = Book(price = f.price.data,
                title = f.title.data,
                url = f.url.data,
                img = f.img.data,
                author_id = a.id)
        db.session.add(n)
        db.session.commit()
        return redirect(url_for("author",id=n.id))
    return render_template(
    "home.html",
    form = f
    )

def delete_author(id):
    del_author(id)
    return redirect(url_for("authors"))


class LoginForm(FlaskForm):
    username= StringField('Username')
    password = PasswordField("Password")
    next = HiddenField()

    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd==user.password else None

@app.route("/login", methods=("GET","POST",))
def login():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data=request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template(
    "login.html",
    form=f
    )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
