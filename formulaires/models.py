from .app import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return "<Author (%d) %s>\n" % (self.id,self.name)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))
    author_id = db.Column(db.Integer,db.ForeignKey("author.id"))
    author = db.relationship("Author",backref=db.backref("books",lazy="dynamic"))

    def __repr__(self):
        return "<Book (%d) %s>\n" % (self.id,self.title)

def get_sample():
    return Book.query.limit(10).all

def get_books(n=None):
    return get_sample(n) if n else Book.query.all()

def get_book(index):
    return Book.query.get_or_404(index)

def get_books_for_author(author):
    return Author.query.filter(Author.name==author).one().books.all()

def get_authors():
    return Author.query.all()

def get_author(id):
    return Author.query.filter(Author.id==id).all()[0]
