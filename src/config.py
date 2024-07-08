import os

from mongomock.mongo_client import MongoClient


class Config:
    MONGODB_SETTINGS = {
        'db': os.environ.get('DB_NAME', 'flask_db'),
        'host': f'mongodb://{os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'root')}:'
                f'{os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'example')}@'
                f'{os.environ.get('DB_HOST', 'localhost')}:'
                f'{os.environ.get('DB_PORT', 27017)}/'
                f'{os.environ.get('DB_NAME', 'flask_db')}?authSource=admin'
    }


class TestConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {
        'db': os.environ.get('DB_NAME', 'flask_db') + '_test',
        'host': 'localhost',
        'mongo_client_class': MongoClient,
        'alias': 'default'
    }
