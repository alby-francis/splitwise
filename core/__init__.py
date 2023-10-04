from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///splitwise.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:qwerty@localhost/splitwise"
app.config['SECRET_KEY'] = "secret_splitwise"
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()
    
from core import routes

