import datetime

from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from mongoengine import ValidationError

from src import logger, LoggerMessageTemplates

from src.user.models import User


class AuthRegister(Resource):
    def post(self):
        try:
            user = User.create_user(**request.json)

            logger.info(LoggerMessageTemplates.get_created_user_log(user))
        except ValidationError as exception:
            logger.error(LoggerMessageTemplates.get_error_log(exception.message, request))
            return {'error': exception.message}, 400

        return {"message": "User has been registered successfully", "created_user": user.to_json()}, 201


class AuthLogin(Resource):
    def get(self):
        auth = request.json

        user = User.get_user_by_email(auth.get('email'))

        if not user or not User.check_password(user, auth.get('password', '')):

            return {'message': 'wrong credentials!'}, 401

        access_token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(hours=1))

        logger.info(LoggerMessageTemplates.get_logged_user_log(user))

        return jsonify(access_token=access_token)
