import click
from .app import app, db


@app.cli.command()
@click.argument('filename1')
@click.argument('filename2')
@click.argument('filename3')
def loaddb(filename1, filename2, filename3):
    '''Creates the tables and populates them with data.'''
    # création de toutes les tables
    db.create_all()  # chargement de notre jeu de données

    import yaml
    data1 = yaml.load(open(filename1))
    data2 = yaml.load(open(filename2))
    data3 = yaml.load(open(filename3))

    # import des modèles
    from .models import Item, Entity, Recipe

    # première passe: création de tous les Items
    items = {}
    for b in data1:  # Pour chaque items
        o = Item(idItem=b["type"],
                 meta=b["meta"],
                 nameItem=b['name'],
                 text_typeItem=b["text_type"]
                 )
        db.session.add(o)
    db.session.commit()
    # deuxième passe: création de tous les entités
    for b in data2:
        o = Entity(idEntity=b['type'],
                   nameEntity=b['name'],
                   text_typeEntity=b['text_type']
                   )
        db.session.add(o)
    db.session.commit()
    # troisieme passe: création de tous les recettes
    for b in data3:
        o = Recipe(idRecipe=b['id'],
                   # Correspond au nom du block en question
                   nameRecipe=b['name'],
                   nameId=b['nameId'],
                   cases=b['cases'],
                   # Correspond à au nombre d'item à la sortie
                   output=b['output']
                   )
        db.session.add(o)
    db.session.commit()


@app.cli.command()
def syncdb():
    """
    Creates all missing tables
    """
    db.create_all()


@app.cli.command()
@click.argument('username')
@click.argument('password')
def newuser(username, password):
    """Adds a new user"""
    from .models import User
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    u = User(username=username, password=m.hexdigest())
    db.session.add(u)
    db.session.commit()


@app.cli.command()
@click.argument('username')
@click.argument('password')
def changepsw(username, password):
    from .models import get_user
    from .models import User
    from hashlib import sha256
    user = get_user(username)
    m = sha256()
    m.update(password.encode())
    user.password = m.hexdigest()
    db.session.commit()
