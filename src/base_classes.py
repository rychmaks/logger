from mongoengine import Document, ValidationError


class BaseModel(Document):
    """
        description:
            Base model class

        methods:
            get_table_name: returns name of the called model.

            are_fields_valid: runs through the given fields and checks
            whether all of them are in the model. If not, raises ValidationError
            that points to the invalid field.
    """
    meta = {'allow_inheritance': True}

    def get_table_name(self) -> str:
        return self._meta['collection']

    @classmethod
    def are_fields_valid(cls, **fields):
        for key, value in fields.items():
            if key not in cls._fields:
                raise ValidationError(f"'{key}' is not a valid field")
