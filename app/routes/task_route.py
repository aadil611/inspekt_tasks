from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.task import create_task, get_tasks, update_task, delete_task
from app.utils.logger import get_logger
from flask_jwt_extended import get_jwt_identity
from app.utils.response import create_response

task_bp = Blueprint("tasks", __name__)
logger = get_logger(__name__)

@task_bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task_route():
    data = request.get_json()
    return create_task(data["title"], data.get("description", ""))


@task_bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks_route():
    return get_tasks()

# get a single task
@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
def get_single_task(task_id: int):
    user_id = get_jwt_identity()
    logger.info(f"User {user_id} fetching task {task_id}")
    return get_tasks(task_id)


@task_bp.route("/tasks/<int:task_id>", methods=["PATCH"])
@jwt_required()
def update_task_route(task_id: int):
    data = request.get_json()
    title, description = data.get("title"), data.get("description")
    is_completed = data.get("is_completed")
    
    if title is None and description is None and is_completed is None:
        return create_response(False, "No data to update", None, 400)
    
    logger.info(f"User {get_jwt_identity()} updating task {task_id} with {data}")
    
    return update_task(task_id, title, description, is_completed)


@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task_route(task_id: int):
    return delete_task(task_id)
