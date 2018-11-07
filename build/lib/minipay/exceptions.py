
__all__ = ['TargetError', 'MethodError', 'ModeError', 'ModelError', 'OpenidError',
           'TooManyArgumentError', 'ProductIdError']


class BaseMiniPayError(Exception):
    pass


class TargetError(Exception):
    """没有请求地址"""
    pass


class MethodError(Exception):
    """请求方法错误"""
    pass


class ModeError(Exception):
    """模式没有设置错误"""
    pass


class ModelError(Exception):
    """模型没有设置"""
    pass


class OpenidError(Exception):
    """openid没有设置"""
    pass


class ProductIdError(Exception):
    """produce_id没有设置"""
    pass


class TooManyArgumentError(Exception):
    """传入了多余的参数"""
    pass
