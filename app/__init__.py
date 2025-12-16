from flask import Blueprint 

master_api = Blueprint('master_api', __name__)

# Import module Blueprints
from app.modules.users.routes import auth_bp
from app.modules.hackathons.routes import hackathon_bp
from app.modules.teams.routes import team_bp
from app.modules.registration.routes import registration_bp
from app.modules.submissions.routes import submission_bp
from app.modules.submissions.judge_routes import judge_bp
from app.modules.winners.routes import winner_bp



# Register module Blueprints
master_api.register_blueprint(auth_bp, url_prefix='/auth')
master_api.register_blueprint(hackathon_bp,url_prefix='/hackathon')
master_api.register_blueprint(team_bp,url_prefix='/team')
master_api.register_blueprint(registration_bp,url_prefix='/register')
master_api.register_blueprint(submission_bp,url_prefix='/submissions')
master_api.register_blueprint(judge_bp)
master_api.register_blueprint(winner_bp)





@master_api.route('/', methods=['GET'])
def welcome():
    return "Welcome to the Proxima"
