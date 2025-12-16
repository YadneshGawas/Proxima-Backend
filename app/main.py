from flask import Flask
from app import master_api
from app.extensions import db, migrate, jwt, bcrypt
from app.config.settings import Config
from app.errors.handlers import register_error_handlers
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    CORS(
    app,
    origins=["http://localhost:8080"],
    supports_credentials=True
    )


     # 🔥 IMPORT ALL MODELS HERE BEFORE MIGRATION
    from app.modules.users.models import User
    from app.modules.hackathons.models import Hackathon,HackathonInterest 
    from app.modules.winners.models import Winner
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(master_api)

    # Register exception handlers
    register_error_handlers(app)
    
    return app