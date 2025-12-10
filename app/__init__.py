from flask import Blueprint 

master_api = Blueprint('master_api', __name__)

# Import module Blueprints
from app.modules.users.routes import auth_bp




# Register module Blueprints
master_api.register_blueprint(auth_bp, url_prefix='/auth')





@master_api.route('/', methods=['GET'])
def welcome():
    return "Welcome to the Proxima"
