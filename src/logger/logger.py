import logging
from typing import Optional

from flask import request

from src.base_classes import BaseModel
from src.logger.models import LoggerModel
from src.user.models import User


class DatabaseHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        LoggerModel.create_log(
            log_file=record.name,
            info_type=record.levelname,
            message=record.msg,
            date_and_time=record.asctime
        )


class LoggerFactory:
    _LOG = None

    @staticmethod
    def __create_logger(log_file: str, log_level: str, log_format: Optional[str] = None):
        """
        A private method that interacts with the python
        logging module
        """
        log_format = log_format or '%(asctime)s [%(levelname)s]: %(message)s'

        # Initialize the class variable with logging object
        LoggerFactory._LOG = logging.getLogger(log_file)
        LoggerFactory._LOG.setLevel(logging.NOTSET)  # Set to NOTSET to handle all levels

        # Create a base logging formatter
        base_formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

        # Create a file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(base_formatter)
        LoggerFactory._LOG.addHandler(file_handler)

        # Create a stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(base_formatter)
        LoggerFactory._LOG.addHandler(stream_handler)

        # Create a database handler
        database_handler = DatabaseHandler()
        stream_handler.setFormatter(base_formatter)
        LoggerFactory._LOG.addHandler(database_handler)

        # Set the logging level based on the user selection
        if log_level == 'INFO':
            LoggerFactory._LOG.setLevel(logging.INFO)
        elif log_level == 'ERROR':
            LoggerFactory._LOG.setLevel(logging.ERROR)
        elif log_level == 'DEBUG':
            LoggerFactory._LOG.setLevel(logging.DEBUG)
        else:
            LoggerFactory._LOG.setLevel(logging.NOTSET)

        return LoggerFactory._LOG

    @staticmethod
    def get_logger(log_file, log_level):
        """
        A static method called by other modules to initialize logging in
        their own module
        """
        logger = LoggerFactory.__create_logger(log_file, log_level)

        return logger


class LoggerMessageTemplates:
    __USER_CREDENTIALS_TEMPLATE = '%(email)s, %(first_name)s %(last_name)s '

    _ERROR = 'Error "%(error)s" occurred in %(endpoint)s with method: %(method)s'
    _AUTHENTICATED_USER_ERROR = (__USER_CREDENTIALS_TEMPLATE +
                                 'got an error "%(error)s" in %(endpoint)s with method: %(method)s')
    _USER_ENTERED_THE_ENDPOINT = __USER_CREDENTIALS_TEMPLATE + 'entered the %(endpoint)s with method: %(method)s'
    _USER_CREATED_THE_TABLE_RECORD = (
            __USER_CREDENTIALS_TEMPLATE +
            'created a new record at %(table_name)s table '
            'with id %(record_id)s in %(endpoint)s'
    )
    _USER_CHANGED_THE_FIELD = (
            __USER_CREDENTIALS_TEMPLATE +
            'changed %(field_name)s'
            ' from %(old_version)s to %(new_version)s at %(table_name)s in %(endpoint)s'
    )
    _USER_DELETED_THE_TABLE_RECORD = (
            __USER_CREDENTIALS_TEMPLATE +
            'deleted record at %(table_name)s table with id %(record_id)s in %(endpoint)s'
    )
    _ENDPOINT_WAS_CALLED = '%(endpoint)s was called with method %(method)s'

    _CREATED_USER = 'User ' + __USER_CREDENTIALS_TEMPLATE + 'was created successfully'
    _USER_LOGGED_IN = 'User ' + __USER_CREDENTIALS_TEMPLATE + 'has logged in'

    @staticmethod
    def get_created_user_log(user: User) -> str:
        return LoggerMessageTemplates._CREATED_USER % {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

    @staticmethod
    def get_logged_user_log(user: User) -> str:
        return LoggerMessageTemplates._USER_LOGGED_IN % {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

    @staticmethod
    def get_error_log(error_message: str, request_instance: request) -> str:
        return LoggerMessageTemplates._ERROR % {
            'error': error_message,
            'endpoint': request_instance.path,
            'method': request_instance.method
        }

    @staticmethod
    def get_error_with_authenticated_user_log(user: User, request_instance: request, error_message: str) -> str:
        return LoggerMessageTemplates._AUTHENTICATED_USER_ERROR % {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'error': error_message,
            'endpoint': request_instance.path,
            'method': request_instance.method
        }

    @staticmethod
    def get_the_endpoint_enter_log(user: User, request_instance: request) -> str:
        return LoggerMessageTemplates._USER_ENTERED_THE_ENDPOINT % {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'method': request_instance.method,
            'endpoint': request_instance.path
        }

    @staticmethod
    def get_created_record_log(user: User, request_instance: request, record: BaseModel) -> str:

        return LoggerMessageTemplates._USER_CREATED_THE_TABLE_RECORD % {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'table_name': record.get_table_name(),
            'record_id': record.id,
            'endpoint': request_instance.path
        }

    @staticmethod
    def get_changed_record_log(
            user: User,
            record: BaseModel,
            new_field_version: dict,
            request_instance: request
    ) -> str:
        old_field_version = {field: record[field] for field in record._fields if field in new_field_version.keys()}

        return LoggerMessageTemplates._USER_CHANGED_THE_FIELD % {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'field_name': list(old_field_version.keys()),
            'old_version': old_field_version,
            'new_version': new_field_version,
            'table_name': record.get_table_name(),
            'record_id': record.id,
            'endpoint': request_instance.path
        }

    @staticmethod
    def get_deleted_record_log(user: User, request_instance: request, record: BaseModel) -> str:
        return LoggerMessageTemplates._USER_DELETED_THE_TABLE_RECORD % {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'table_name': record.get_table_name(),
            'record_id': record.id,
            'endpoint': request_instance.path
        }

    @staticmethod
    def get_endpoint_was_called_log(request_instance: request,) -> str:
        return LoggerMessageTemplates._ENDPOINT_WAS_CALLED % {
            'endpoint': request_instance.path,
            'method': request_instance.method
        }
