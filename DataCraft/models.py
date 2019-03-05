from .app import login_manager
from .app import db
from flask_login import UserMixin


class Item(db.Model):
    idItem = db.Column(db.Integer, primary_key=True)
    meta = db.Column(db.Integer, primary_key=True)
    nameItem = db.Column(db.String(100))
    text_typeItem = db.Column(db.String(100))
    description = db.Column(db.String(1000))

    def __repr__(self):
        return "<Block (%d) %s>\n" % (self.idItem, self.nameItem)


class Entity(db.Model):
    idEntity = db.Column(db.Integer, primary_key=True)
    nameEntity = db.Column(db.String(100))
    text_typeEntity = db.Column(db.String(100))

    def __repr__(self):
        return "<Entity (%d) %s>\n" % (self.idEntity, self.nameEntity)


class Recipe(db.Model):
    idRecipe = db.Column(db.Integer, primary_key=True)
    nameRecipe = db.Column(db.String(100))
    nameId = db.Column(db.Integer)
    cases = db.Column(db.String(200))
    output = db.Column(db.Integer)

    def __repr__(self):
        return "<%d Recipe (%s) %s>\n" % (self.idRecipe, self.cases, self.nameRecipe)


class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))

    def get_id(self):
        return self.username


def get_block_sample(n):
    return Item.query.limit(n).all()


def get_block_sample(n):
    return Entity.query.limit(n).all()


def get_recipe_sample(n):
    return Recipe.query.limit(n).all()


def get_blocks(n=None):
    return get_block_sample(n) if n else Item.query.all()


def get_blocks_list():
    data = Item.query.all()
    res = []
    for x in data:
        res.append((str(x.idItem) + '-' + str(x.meta), x.nameItem))
    return res


def get_block_name(id):
    idI, m = id.split("-")
    block = Item.query.filter(Item.idItem == idI, Item.meta == m).one()
    return block.nameItem

def get_block(id):
    idI, m = id.split("-")
    block = Item.query.filter(Item.idItem == idI, Item.meta == m).one()
    return block

def get_entities(n=None):
    return get_entity_sample(n) if n else Entity.query.all()


def get_recipes(n=None):
    return get_recipe_sample(n) if n else Recipe.query.all()


def form_convert_dict(listCase):
    res = {}
    for x in range(9):
        res[x + 1] = (get_block_name(listCase[x]), listCase[x])
    return str(res)

def getCraftFromBlock(id):
    pass
    #
    #Récuperer via jointure entre craft et block les craft contenant ce block en recipe
    #

def getCraftForBlock(id):
    pass
    #
    #Retourne les output qui correspondent au bloc
    #

#
# def get_book(index):
#     return Book.query.get_or_404(index)
#
# def get_books_for_author(author):
#     return Author.query.filter(Author.name==author).one().books.all()
#
# def get_authors():
#     return Author.query.all()
#
# def get_author(id):
#     return Author.query.get(id)
#
# def del_author(id):
#     User.query.filter_by(id).delete()
#     db.commit()


@login_manager.user_loader
def get_user(user):
    return User.query.get(user)
