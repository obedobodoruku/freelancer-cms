from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "6d6cdfdfe0ed4f9c88d4338a3cff2d9757f138947263b14188e2d72498921ba4"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
Migrate(app, db)
login_manager = LoginManager(app)

from app import routes
from app import models