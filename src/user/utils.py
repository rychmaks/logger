from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from src.base_classes import BaseModel
from src.user.models import User


def jwt_optional(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
            current_user = get_jwt_identity()
            if not current_user:
                return {'message': 'Authorization required'}, 401
        except Exception as e:

            return {'message': 'Authorization required'}, 401

        return fn(*args, **kwargs)

    return wrapper


def get_user_instance_by_jwt_token() -> BaseModel:
    current_user_id = get_jwt_identity()

    user = User.get_user_by_id(current_user_id)

    return user
