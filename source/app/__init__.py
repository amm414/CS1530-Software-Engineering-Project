from flask import Flask, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit


print("APP NAME: " + str(__name__))
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db.init_app(app)
socketio = SocketIO(app)


from app import routes, models
