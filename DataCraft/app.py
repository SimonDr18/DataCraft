from flask import Flask
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

app=Flask(__name__)
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['png'])
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="b58c673d-fc5c-4599-9d08-0027fb49e803"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Bootstrap(app)

import os.path
def mkpath(p):
	return os.path.normpath(os.path.join(os.path.dirname(__file__),p))

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../myapp.db'))
db = SQLAlchemy(app)

from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"