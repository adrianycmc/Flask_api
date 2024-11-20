import os
import click
from flask import Flask, current_app
from flask_migrate import Migrate
from controllers import user, auth, role
from flask_jwt_extended import JWTManager
from models.base import db
from extensions import bcrypt
from flask import json
from werkzeug.exceptions import HTTPException
from extensions import ma

migrate = Migrate()
jwt = JWTManager()

def create_app(environment=os.environ["ENVIRONMENT"]):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"config.{environment.capitalize()}Config")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # iniciando a extensão
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    # registro do blueprint
    app.register_blueprint(user.user_bp)
    # app.register_blueprint(post.user_bp)
    app.register_blueprint(auth.user_bp)
    app.register_blueprint(role.user_bp)
    

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response
    
    return app
 
 