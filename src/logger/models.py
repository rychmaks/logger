from typing import override

from mongoengine import Document, StringField, DateTimeField


class LoggerModel(Document):
    log_file = StringField()
    info_type = StringField(choices=['INFO', 'ERROR', 'WARNING', 'CRITICAL'])
    message = StringField(max_length=512)
    date_and_time = DateTimeField()

    @classmethod
    def create_log(cls, **kwargs):
        log = cls(**kwargs)
        log.save()

        return log

    @override
    def to_json(self, *args, **kwargs):
        return {
            'log_id': str(self.id),
            'log_file': self.log_file,
            'log_type': self.info_type,
            'message': self.message,
            'data_and_time': self.date_and_time
        }
