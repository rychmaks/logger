from typing import override

from mongoengine import StringField, ValidationError
from bcrypt import hashpw, gensalt, checkpw

from src.base_classes import BaseModel


class User(BaseModel):
    email = StringField(required=True, unique=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    password = StringField(max_length=256, required=True)

    def set_password(self, password) -> None:
        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        self.password = hashed_password.decode('utf-8')

    def check_password(self, password: str) -> bool:
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @classmethod
    def get_user_by_id(cls, id: str) -> BaseModel:
        return cls.objects(id=id).first()

    @classmethod
    def get_user_by_email(cls, email: str) -> BaseModel:
        return cls.objects(email=email).first()

    @classmethod
    def create_user(cls, **kwargs) -> BaseModel:
        if not kwargs['email'] or not kwargs['password']:
            raise ValidationError('Email and Password fields are required!')

        is_email_taken = True if cls.get_user_by_email(kwargs['email']) else False

        if is_email_taken:
            raise ValidationError('Email is already taken!')

        password = kwargs.pop('password')

        created_user = cls(**kwargs)
        created_user.set_password(password)
        created_user.save()

        return created_user

    @override
    def to_json(self, *args, **kwargs) -> dict:
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
