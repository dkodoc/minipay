
__all__ = ['TargetError', 'MethodError']


class BaseMiniPayError(Exception):
    pass


class TargetError(Exception):
    pass


class MethodError(Exception):
    pass
