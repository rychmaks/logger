from typing import override, Iterable

from mongoengine import StringField, ReferenceField, CASCADE, ValidationError

from src.base_classes import BaseModel
from src.user.models import User


class Posts(BaseModel):
    title = StringField(max_length=64, required=True, null=False, min_length=1)
    text = StringField(max_length=512, required=True, null=False, min_length=1)
    author = ReferenceField(User, required=True, null=False, reverse_delete_rule=CASCADE)

    @override
    def to_json(self, *args, **kwargs) -> dict:
        return {
            'id': str(self.id),
            'title': self.title,
            'text': self.text,
            'author': str(self.author.id)
        }

    @classmethod
    def make_a_post(cls, **kwargs) -> BaseModel:
        cls.are_fields_valid(**kwargs)

        created_post = cls(**kwargs)

        created_post.save()

        return created_post

    @classmethod
    def get_post_by_id(cls, post_id: str) -> BaseModel:
        post = cls.objects(id=post_id).first()

        if not post:
            raise ValidationError(f'Post with id {post_id} does not exist!')

        return post

    @classmethod
    def get_all_posts(cls) -> Iterable[BaseModel]:
        return cls.objects().all()

    def verify_users_access(self, user: User) -> None:
        if self.author != user:
            raise ValidationError('You have no access to do this action!')

    def update_fields(self, user: User, **kwargs) -> None:
        self.are_fields_valid(**kwargs)

        self.verify_users_access(user)

        self.update(**kwargs)

    def delete_post(self, user: User) -> None:
        self.verify_users_access(user)

        self.delete()
