
__all__ = ['TargetError', 'MethodError', 'ModeError', 'ModelError', 'OpenidError',
           'TooManyArgumentError', 'ProductIdError']


class BaseMiniPayError(Exception):
    pass


class TargetError(Exception):
    pass


class MethodError(Exception):
    pass


class ModeError(Exception):
    pass


class ModelError(Exception):
    pass


class OpenidError(Exception):
    pass


class ProductIdError(Exception):
    pass


class TooManyArgumentError(Exception):
    pass
