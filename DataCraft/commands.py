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
    """
    Commande utilisée pour le changement de mot de passe. Entrez le username, puis son nouveau mot de passe.
    """
    from .models import get_user
    from .models import User
    from hashlib import sha256
    user = get_user(username)
    m = sha256()
    m.update(password.encode())
    user.password = m.hexdigest()
    db.session.commit()


@app.cli.command()
@click.argument('file')
def convert(file):
    """
    Commande utilisée pour recupérer tous les noms d'un .xml avec le 'tag <name>'
    """
    f = open("name.txt", "w+")
    import yaml
    data = yaml.load(open(file))
    for b in data :
        f.write(b["name"]+"\n")
    f.close()


@app.cli.command()
def screenGetter():
    """
    Commande utilisant BeautifulSoup, module de parsing, afin de récupérer les images d'un site web automatiquement.
    """
    pass
    
    #TODO Importer BeautifulSoup
    #
    #Recupérer tous les noms d'un fichier .txt et les mettre dans une liste.
    #while (list<=i):
    #   try :
    #      Recuperer l'url du site avec chaque name
    #       Recupérer l'url d'image de l'objet en question dans une div en particulier
    #       Télécharger l'url .png valide coupé sans la version ?
    #   catch :
    #       i non trouvé url invalide
    #
    #Sinon stocket l'url dans la base de donnée et la reutiliser par la suite ? Voir au niveaux des perfs
