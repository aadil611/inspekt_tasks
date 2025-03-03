from flask import Flask
from dotenv import load_dotenv
from app.config import DevConfig
from app.extentions import db, migrate, bcrypt, jwt
from app.routes.auth_route import auth_bp
from app.routes.task_route import task_bp
from app.routes.web_route import web_bp
from flask_cors import CORS
import os


load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=os.getenv("ALLOWED_ORIGINS"))

    @app.get("/health")
    def _():
        return {"success": True}

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(task_bp, url_prefix="/api")
    app.register_blueprint(web_bp)

    return app
