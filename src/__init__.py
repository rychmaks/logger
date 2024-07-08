import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_mongoengine import MongoEngine

from src.config import Config
from src.logger.logger import LoggerFactory, LoggerMessageTemplates

logger = LoggerFactory.get_logger('logging/py.log', 'INFO')


app = Flask(__name__)

app.config.from_object(Config)
db = MongoEngine(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'you-will-never-know')
jwt = JWTManager(app)
api = Api(app)

from src.logger.views import logs
from src import routes
