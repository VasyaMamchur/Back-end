from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .db_func import get_db_connection, create_tables
from flask_jwt_extended import JWTManager
from flask_restful import Api
import mymodule.views
import mymodule.models
import os


app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
create_tables()
app.config.from_pyfile('config.py', silent=True)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['JWT_ALGORITHM'] = "HS256"
jwt = JWTManager(app)
api = Api(app)


