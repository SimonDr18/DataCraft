from .app import app
from flask import render_template
from .models import *
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired
from flask import url_for, redirect, request
from .app import db
from hashlib import sha256
from flask_login import login_user, current_user, logout_user, login_required
import ast


@app.route("/")
def home():
    return render_template(
        "home.html",
        title="DataCraft : Le Mini-Wiki",
        data=get_blocks()
    )


@app.route("/blocks")
def blocks():
    return render_template(
        "blocks.html",
        title="DataCraft : Le Mini-Wiki",
        data=get_blocks()
    )


@app.route("/crafting")
def crafting():
    dico = []
    for i in get_recipes():  # La requete retourne une liste de recipe
        # On transforme la string 'cases' en dictionnaire utilisable
        dico.append(ast.literal_eval(i.cases))
    return render_template(
        "crafting.html",
        title="Les Crafts disponibles",
        data=get_recipes(),
        dico=dico
    )


@app.route("/entities")
def entities():
    return render_template(
        "entities.html",
        title="Les entitées du jeu",
        data=get_entities()
    )


class BlockForm(FlaskForm):
    id = HiddenField('id')
    idItem = IntegerField('ID du Block', validators=[DataRequired()])
    blockmeta = StringField('Meta-data du Block', validators=[DataRequired()])
    name = StringField('Nom', validators=[DataRequired()])
    text_type = StringField('Type', validators=[DataRequired()])


class EntityForm(FlaskForm):
    id = HiddenField('id')
    entityid = StringField("ID de l'entité", validators=[DataRequired()])
    name = StringField('Nom', validators=[DataRequired()])
    text_type = StringField('Type', validators=[DataRequired()])


class CraftingForm(FlaskForm):
    id = HiddenField('id')
    craftingid = StringField('ID du Block', validators=[DataRequired()])
    name = StringField('Nom', validators=[DataRequired()])
    case1 = SelectField("case 1", choices=get_blocks_list(),
                        validators=[DataRequired()])
    case2 = SelectField("case 2", choices=get_blocks_list(),
                        validators=[DataRequired()])
    case3 = SelectField("case 3", choices=get_blocks_list(),
                        validators=[DataRequired()])
    case4 = SelectField("case 4", choices=get_blocks_list(),
                        validators=[DataRequired()])
    case5 = SelectField("case 5", choices=get_blocks_list(),
                        validators=[DataRequired()])
    case6 = SelectField("case 6", choices=get_blocks_list(),
                        validators=[DataRequired()])
    case7 = SelectField("case 7", choices=get_blocks_list(),
                        validators=[DataRequired()])
    case8 = SelectField("case 8", choices=get_blocks_list(),
                        validators=[DataRequired()])
    case9 = SelectField("case 9", choices=get_blocks_list(),
                        validators=[DataRequired()])
    output = StringField("Nombre d'items en sortie",
                         validators=[DataRequired()])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))


@app.route("/add/block")
def add_block():
    f = BlockForm()
    return render_template(
        "add_block.html",
        form=f
    )


@app.route("/create/block", methods=("POST",))
def add_block_POST():
    n = None
    f = BlockForm()
    if f.validate_on_submit():
        n = Item(idItem=f.idItem.data,
                 meta=f.blockmeta.data,
                 nameItem=f.name.data,
                 text_typeItem=f.text_type.data)
        db.session.add(n)
        db.session.commit()
        return redirect(url_for("blocks"))
    return render_template(
        "add_block.html",
        form=f
    )


@app.route("/add/entity")
def add_entity():
    f = EntityForm()
    return render_template(
        "add_entity.html",
        form=f
    )


@app.route("/create/entity", methods=("POST",))
def add_entity_POST():
    n = None
    f = EntityForm()
    if f.validate_on_submit():
        n = Entity(idEntity=f.entityid.data,
                   nameEntity=f.name.data,
                   text_typeEntity=f.text_type.data)
        db.session.add(n)
        db.session.commit()
        return redirect(url_for("entities"))
    return render_template(
        "add_entity.html",
        form=f
    )


@app.route("/add/crafting")
def add_crafting():
    f = CraftingForm()
    return render_template(
        "add_crafting.html",
        form=f
    )


@app.route("/create/crafting", methods=("POST",))
def add_crafting_POST():
    n = None
    f = CraftingForm()
    if f.validate_on_submit():
        list = [f.case1.data, f.case2.data, f.case3.data, f.case4.data,
                f.case5.data, f.case6.data, f.case7.data, f.case8.data, f.case9.data]
        dico = form_convert_dict(list)
        n = Recipe(nameRecipe=f.name.data,
                   nameId=f.craftingid.data,
                   cases=dico,
                   output=f.output.data)
        db.session.add(n)
        db.session.commit()
        return redirect(url_for("crafting"))
    return render_template(
        "add_crafting.html",
        form=f
    )


@app.route("/mod/block")
def del_block():
    return render_template(
        "mod_block.html",
        title="Menu de gestion des block",
        data=get_blocks()
    )


@app.route("/remove/block", methods=("POST",))
def del_block_POST():
    abort(501)


@app.route("/mod/entity")
def del_entity():
    return render_template(
        "mod_entity.html",
        title="Menu de gestion des entitées",
        data=get_entities()
    )


@app.route("/remove/entity", methods=("POST",))
def del_entity_POST():
    abort(501)


@app.route("/mod/crafting")
def del_crafting():
    return render_template(
        "mod_crafting.html",
        title="Menu de gestion des recettes"
    )


@app.route("/remove/crafting", methods=("POST",))
def del_crafting_POST():
    abort(501)

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField("Password")
    next = HiddenField()

    def get_authenticated_user(self):

        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

class SignInForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField("Password")
    passwordConfirmation = PasswordField('Confirm Password')
    next = HiddenField()

    def write_user_database(self):
        m = sha256()
        m.update(self.password.data.encode())
        u = User(username=self.username.data, password=m.hexdigest())
        db.session.add(u)
        db.session.commit()
        return u

@app.route("/login", methods=("GET", "POST",))
def login():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template(
        "login.html",
        form=f
    )

@app.route("/signin", methods=("GET", "POST",))
def signin():
    f = SignInForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.write_user_database()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template(
        "signin.html",
        form=f
    )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
