from flask import Blueprint, request
from app.services.auth import create_user, login_user
from app.utils.response import create_response
from app.utils.logger import get_logger

auth_bp = Blueprint("auth", __name__)
logger = get_logger(__name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if not data:
            logger.warning("Invalid or Missing json")
            return create_response(False, "Invalid or Missing json", None, 400)
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            
            return create_response(False, "Username and password are required", None, 400)
            
        return create_user(data["username"], data["password"])
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return create_response(False, str(e), None, 500)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return create_response(False, "Username and password are required", None, 400)
    return login_user(data["username"], data["password"])
