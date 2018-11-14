import yaml
import os.path
import random

BOOKS=yaml.load(open(os.path.join(os.path.dirname(__file__),"data.yml")))

def get_books(n=None):
    return random.sample(BOOKS,n) if n else BOOKS

def get_book(index):
    return BOOKS[index]

def get_books_for_author(author):
    res = []
    for livre in BOOKS :
        if livre["author"]==author:
            res.append(livre["title"])
    return "<br>".join(res)
