class MiniAppsConfig:
    APP_ID = None
    MCH_ID = None
    SECRET = None
    NONCE_STR = None
    KEY = None

    # 支付通知和退款通知，根据自己的后台接口填写
    PAYMENT_NOTIFY_URL = None
    REFUND_NOTIFY_URL = None

    # 微信退款需要用到的商户证书，没有配置的话请求退款会出错
    # 详情见：https://pay.weixin.qq.com/wiki/doc/api/wxa/wxa_api.php?chapter=4_3
    # 例如
    # CERT = '/appclient.pem'
    # CERT_KEY = '/appclient_key.pem'
    CERT = ''
    CERT_KEY = ''

    # 默认模式， 目前有 ignore 和 store， store则必须提供ORM模型类用来保存请求和响应记录
    # 目前之支持Django2.0以上版本
    DEFAULT_MODE = 'ignore'

    # 默认的ORM模型类，可以到用的时候再填
    DEFAULT_MODEL = None

    # 默认请求方法 post or get
    DEFAULT_METHOD = 'post'

    # 是否使用异步请求
    ASYNC = False

    # 如果微信接口不更新，下面的不用更改
    API_UNIFIED_ORDER = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    API_ORDER_QUERY = "https://api.mch.weixin.qq.com/pay/orderquery"
    API_CLOSE_ORDER = "https://api.mch.weixin.qq.com/pay/closeorder"
    API_REFUND = "https://api.mch.weixin.qq.com/secapi/pay/refund"
    API_REFUND_QUERY = "https://api.mch.weixin.qq.com/pay/refundquery"
