class MiniAppsConfig(object):
    """
    MiniApps config
    """
    APP_ID = None
    MCH_ID = None
    SECRET = None
    NONCE_STR = None
    KEY = None
    PAYMENT_NOTIFY_URL = None
    REFUND_NOTIFY_URL = None
    DEFAULT_MODE = 'ignore'
    DEFAULT_METHOD = 'post'
    API_UNIFIED_ORDER = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    API_ORDER_QUERY = "https://api.mch.weixin.qq.com/pay/orderquery"
    API_CLOSE_ORDER = "https://api.mch.weixin.qq.com/pay/closeorder"
    API_REFUND = "https://api.mch.weixin.qq.com/secapi/pay/refund"
    API_REFUND_QUERY = "https://api.mch.weixin.qq.com/pay/refundquery"
