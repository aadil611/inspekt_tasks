from flask import Blueprint, render_template, redirect, request, session, url_for
import requests
from app.utils.logger import get_logger
from flask import flash

web_bp = Blueprint("web", __name__)
logger = get_logger(__name__)

API_URL = "http://localhost:5000/api"

@web_bp.route("/")
def index():
    return render_template("tasks.html", tasks=[])
