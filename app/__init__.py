from flask import Flask
from dotenv import load_dotenv
from app.config import DevConfig
from app.extentions import db, migrate, bcrypt, jwt
from app.routes.auth_route import auth_bp


load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.get("/health")
    def _():
        return {"success": True}

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
