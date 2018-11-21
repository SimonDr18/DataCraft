from flask import Flask
from flask_bootstrap import Bootstrap
app=Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

import os.path
def mkpath(p):
	return os.path.normpath(os.path.join(os.path.dirname(__file__),p))

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../myapp.db'))
db = SQLAlchemy(app)
