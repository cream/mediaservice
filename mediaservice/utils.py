from sqlalchemy.orm import validates

class TypeNotSupported(TypeError):
    pass

def simple_validator(field, validator_func):
    def _validate(self, key, val):
        assert validator_func(val)
        return val
    return validates(field)(_validate)
