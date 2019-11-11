from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


print("APP NAME: " + str(__name__))
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db.init_app(app)


from app import routes, models
