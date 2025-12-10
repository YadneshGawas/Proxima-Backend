from flask import Flask
from app import master_api
from app.extensions import db, migrate, jwt, bcrypt
from app.config.settings import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(master_api)
    
    return app