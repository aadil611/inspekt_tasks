from flask_jwt_extended import get_jwt_identity
from typing import Any, Dict, Tuple
from app.models.task import Task, db
from app.utils.response import create_response
from app.utils.logger import get_logger

logger = get_logger(__name__)

def create_task(title: str, description: str) -> Tuple[Dict[str, Any], int]:
    """ create a task for logged-in user """
    user_id = get_jwt_identity()
    logger.info(f"User {user_id} creating task: {title}")

    task = Task(title=title, description=description, user_id=user_id)
    db.session.add(task)
    db.session.commit()

    logger.info(f"Task '{task.title}' created successfully for user {user_id}")
    return create_response(True, "Task created successfully", {"task_id": task.id}, 201)


def get_tasks(task_id: int = None) -> Tuple[Dict[str, Any], int]:
    """ list all tasks for current logged-in user """
    user_id = get_jwt_identity()
    logger.info(f"User {user_id} fetching their tasks")
    tasks = Task.query.filter_by(user_id=user_id).all()
    
    if task_id:
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            logger.warning(f"User {user_id} tried fetching a non-existent task {task_id}")
            return create_response(False, "Task not found", None, 404)
        task_data = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_completed": task.is_completed
        }
        return create_response(True, "Task fetched successfully", task_data, 200)
    
    tasks = Task.query.filter_by(user_id=user_id).all()
    logger.info(f"User {user_id} fetched their tasks")
    task_list = [{"id": t.id, "title": t.title, "description": t.description, "is_completed": t.is_completed} for t in tasks]

    return create_response(True, "Tasks fetched successfully", {"tasks": task_list}, 200)


def update_task(task_id: int, title: str, description: str, is_completed: bool) -> Tuple[Dict[str, Any], int]:
    """ Update a task owned by the logged-in user """
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        logger.warning(f"User {user_id} tried updating a non-existent task {task_id}")
        return create_response(False, "Task not found", None, 404)
    
    if title:
        task.title = title
    if description:
        task.description = description
    if is_completed is not None:
        task.is_completed = is_completed

    db.session.commit()

    logger.info(f"Task {task_id} updated successfully by user {user_id}")
    return create_response(True, "Task updated successfully", {"data": {"is_completed": task.is_completed}}, 200)


def delete_task(task_id: int) -> Tuple[Dict[str, Any], int]:
    """ Delete a task owned by the logged-in user """
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        logger.warning(f"User {user_id} tried deleting a non-existent task {task_id}")
        return create_response(False, "Task not found", None, 404)

    db.session.delete(task)
    db.session.commit()

    logger.info(f"Task {task_id} deleted successfully by user {user_id}")
    return create_response(True, "Task deleted successfully", None, 209)
