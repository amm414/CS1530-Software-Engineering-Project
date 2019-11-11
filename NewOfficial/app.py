from flask import Flask, redirect, render_template
import os

app = Flask(__name__)

# configuration
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'CraigVersity.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(__name__)