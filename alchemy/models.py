from .app import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))
    author_id = db.Column(db.Integer,db.ForeignKey("author.id"))
    author = db.relationship("Author",backref=db.backref("books",lazy="dynamic"))

def get_sample():
    return Book.query.limit(10).all

# def get_books(n=None):
#     return random.sample(BOOKS,n) if n else BOOKS
#
# def get_book(index):
#     return BOOKS[index]
#
# def get_books_for_author(author):
#     res = []
#     for livre in BOOKS :
#         if livre["author"]==author:
#             res.append(livre["title"])
#     return "<br>".join(res)
