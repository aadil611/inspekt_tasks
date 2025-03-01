from flask import jsonify
from app.utils.logger import get_logger
from typing import Any, Dict, Tuple

logger = get_logger(__name__)


def create_response(
    success: bool, message: str, data: Any = None, status_code: int = 200
) -> Tuple[Any, int]:
    """consistent response structure"""
    response_body: Dict[str, Any] = {"success": success, "message": message}

    if data:
        response_body["data"] = data

    if success:
        logger.info(f"Response -> {status_code}: {message}")
    else:
        logger.warning(f"Response -> {status_code}: {message}")

    return jsonify(response_body), status_code
