from flask import request
from flask_restful import Resource
from mongoengine import ValidationError

from src import logger, LoggerMessageTemplates
from src.posts.models import Posts
from src.user.utils import jwt_optional, get_user_instance_by_jwt_token


class PostsCollectionView(Resource):
    def get(self):
        logger.info(LoggerMessageTemplates.get_endpoint_was_called_log(request))

        posts = Posts.get_all_posts()

        return {'posts': posts.to_json()}, 200

    @jwt_optional
    def post(self):
        request_data = request.json
        current_user = get_user_instance_by_jwt_token()

        try:
            post = Posts.make_a_post(**request_data, author=current_user)

            logger.info(
                LoggerMessageTemplates.get_created_record_log(
                    current_user,
                    request,
                    post
                )
            )
        except ValidationError as exception:
            logger.error(
                LoggerMessageTemplates.get_error_with_authenticated_user_log(
                    current_user,
                    request,
                    exception.message
                )
            )
            return {'error': exception.message}, 400

        return {'message': 'Post was successfuly created!', 'post': post.to_json()}, 200


class PostsDetailedView(Resource):
    def get(self, post_id: str):
        logger.info(LoggerMessageTemplates.get_endpoint_was_called_log(request))

        posts = Posts.get_post_by_id(post_id)

        return {'posts': posts.to_json()}, 200

    @jwt_optional
    def patch(self, post_id: str):
        current_user = get_user_instance_by_jwt_token()
        data = request.json

        try:
            post = Posts.get_post_by_id(post_id)
            post.update_fields(current_user, **data)

            logger.info(
                LoggerMessageTemplates.get_changed_record_log(
                    current_user,
                    post,
                    data,
                    request
                )
            )
            post.reload()
        except ValidationError as exception:
            logger.error(
                LoggerMessageTemplates.get_error_with_authenticated_user_log(
                    current_user,
                    request,
                    exception.message
                )
            )
            return {'error': exception.message}, 400

        return {'message': 'Post was successfuly updated!', 'post': post.to_json()}, 200

    @jwt_optional
    def delete(self, post_id: str):
        current_user = get_user_instance_by_jwt_token()

        try:
            post = Posts.get_post_by_id(post_id)
            post.delete_post(current_user)

            logger.info(
                LoggerMessageTemplates.get_deleted_record_log(
                    current_user,
                    request,
                    post
                )
            )
        except ValidationError as exception:
            logger.error(
                LoggerMessageTemplates.get_error_with_authenticated_user_log(
                    current_user,
                    request,
                    exception.message
                )
            )
            return {'error': exception.message}, 400

        return {'message': 'Post was successfuly deleted!'}, 200
