from app.models.user import User
from app.extentions import db, bcrypt
from flask_jwt_extended import create_access_token
from typing import Optional, Any, Tuple
from flask import jsonify
from app.utils.logger import get_logger
from app.utils.response import create_response
from datetime import timedelta

logger = get_logger(__name__)


def create_user(username: str, password: str) -> Tuple[Any, int]:
    "create and return a User Object with hashed password"
    logger.info(f"creating user: {username}")

    if User.query.filter_by(username=username).first():
        logger.warning("User creation failed: User '{username}' already exists")
        return create_response(False, "User already Exists", None, 400)

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()

    logger.info(f"User {username} created successfully")
    return create_response(True, "User created successfully", {"id": user.id}, 201)


def login_user(username: str, password: str) -> Tuple[Any, int]:
    """match username and password, if correct generate token"""
    logger.info(f"user '{username}' tried to login")

    user: Optional[User] = User.query.filter_by(username=username).first()
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    if user is None or not bcrypt.check_password_hash(user.password_hash, password):
        logger.warning(
            f"User loging failer for '{username}' -> invalid username or password"
        )
        return create_response(False, "invalid username or password", None, 401)

    access_token = create_access_token(
        identity=str(user.id), expires_delta=timedelta(hours=1)
    )
    logger.info(f"User '{username}' logged in successfully")
    return create_response(
        True, "User Loggedin successfully", {"access_token": access_token}, 200
    )
