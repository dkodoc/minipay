import re
import base64
from hashlib import md5
from Crypto.Cipher import AES

from minipay.exceptions import (
    OpenidError,
    TooManyArgumentError,
    ProductIdError
)
from minipay.base import BaseMiniPay, BaseNotification


class UnifiedOrder(BaseMiniPay):
    """
    doc: https://pay.weixin.qq.com/wiki/doc/api/wxa/wxa_api.php?chapter=9_1
    """

    def __init__(self, out_trade_no, body, total_fee,
                 device_info=None, detail=None, attach=None, fee_type=None,
                 time_start=None, time_expire=None, goods_tag=None, limit_pay=None,
                 openid=None, spbill_create_ip=None, trade_type=None, notify_url=None,
                 product_id=None, **kwargs):
        super(UnifiedOrder, self).__init__(**kwargs)
        self.target = kwargs.get('target') or self.config['api_unified_order']
        self.notify_url = notify_url or self.config['payment_notify_url']
        self.request_data = {
            'appid': self.config['app_id'],
            'mch_id': self.config['mch_id'],
            'device_info': device_info,
            'nonce_str': self.config['nonce_str'],
            'sign': None,
            'sign_type': None,
            'body': body,
            'detail': detail,
            'attach': attach,
            'out_trade_no': out_trade_no,
            'fee_type': fee_type,
            'total_fee': total_fee,
            'spbill_create_ip': spbill_create_ip or '47.94.162.104',
            'time_start': time_start,
            'time_expire': time_expire,
            'goods_tag': goods_tag,
            'notify_url': self.notify_url,
            'trade_type': trade_type or 'JSAPI',
            'product_id': product_id,
            'limit_pay': limit_pay,
            'openid': openid
        }

    def _decision_rules(self):
        if self.request_data['trade_type'] == 'JSAPI':
            if self.request_data['openid'] is None:
                raise OpenidError(
                    "request nimiapps api to unified order need 'openid' parameter when 'trade_type' is 'JSAPI'.")
        if self.request_data['trade_type'] == 'NATIVE':
            if self.request_data['product_id'] is None:
                raise ProductIdError(
                    "request nimiapps api to unified order need 'product_id' parameter when 'trade_type' is 'NATIVE'.")


class OrderQuery(BaseMiniPay):
    def __init__(self, out_trade_no=None, transaction_id=None, **kwargs):
        super(OrderQuery, self).__init__(**kwargs)
        self.target = kwargs.get('target') or self.config['api_order_query']
        self.request_data = {
            'appid': self.config['app_id'],
            'mch_id': self.config['mch_id'],
            'nonce_str': self.config['nonce_str'],
            'transaction_id': transaction_id,
            'out_trade_no': out_trade_no,
            'sign': None,
            'sign_type': None
        }

    def _decision_rules(self):
        if self.request_data['transaction_id'] is None and self.request_data['out_trade_no'] is None:
            raise TypeError("You must choose one from transaction_id or out_trade_no.")
        if self.request_data['transaction_id'] and self.request_data['out_trade_no']:
            raise TooManyArgumentError(
                "You can only choose one from transaction_id or out_trade_no.")


class CloseOrder(BaseMiniPay):
    def __init__(self, out_trade_no, **kwargs):
        super(CloseOrder, self).__init__(**kwargs)
        self.target = kwargs.get('target') or self.config['api_close_order']
        self.request_data = {
            'appid': self.config['app_id'],
            'mch_id': self.config['mch_id'],
            'out_trade_no': out_trade_no,
            'nonce_str': self.config['nonce_str'],
            'sign': None,
            'sign_type': None
        }


class Refund(BaseMiniPay):
    def __init__(self, out_refund_no, total_fee, refund_fee, notify_url=None,
                 refund_desc=None, transaction_id=None, out_trade_no=None,
                 refund_account=None, **kwargs):
        super(Refund, self).__init__(**kwargs)
        self.target = kwargs.get('target') or self.config['api_refund']
        self.notify_url = notify_url or self.config['refund_notify_url']
        self.options.setdefault(
            'cert', (self.config['cert'], self.config['cert_key'])
        )
        self.request_data = {
            'appid': self.config['app_id'],
            'mch_id': self.config['mch_id'],
            'nonce_str': self.config['nonce_str'],
            'sign': None,
            'sign_type': None,
            'transaction_id': transaction_id,
            'out_trade_no': out_trade_no,
            'out_refund_no': out_refund_no,
            'total_fee': total_fee,
            'refund_fee': refund_fee,
            'refund_desc': refund_desc,
            'refund_account': refund_account,
            'notify_url': self.notify_url
        }

    def _decision_rules(self):
        if self.request_data['transaction_id'] is None and self.request_data['out_refund_no'] is None:
            raise TypeError('You must choose one from transaction_id and out_trade_no.')
        if self.request_data['transaction_id'] and self.request_data['out_trade_no']:
            raise TooManyArgumentError("You can only choose one from transaction_id and out_trade_no.")


class RefundQuery(BaseMiniPay):
    """
    doc: https://pay.weixin.qq.com/wiki/doc/api/wxa/wxa_api.php?chapter=9_5
    """

    def __init__(self, transaction_id=None, out_trade_no=None, out_refund_no=None,
                 refund_id=None, offset=None, **kwargs):
        super(RefundQuery, self).__init__(**kwargs)
        self.target = kwargs.get('target') or self.config['api_refund_query']
        self.request_data = {
            'appid': self.config['app_id'],
            'mch_id': self.config['mch_id'],
            'nonce_str': self.config['nonce_str'],
            'sign': None,
            'sign_type': None,
            'transaction_id': transaction_id,
            'out_trade_no': out_trade_no,
            'out_refund_no': out_refund_no,
            'refund_id': refund_id,
            'offset': offset
        }

    def _decision_rules(self):
        if self.request_data['transaction_id'] is None and \
                self.request_data['out_refund_no'] is None and \
                self.request_data['out_trade_no'] is None and \
                self.request_data['refund_id'] is None:
            raise TypeError(
                "You must choose one from 'transaction_id','out_refund_no','out_trade_no', 'refund_id")

        metex_args = [
            self.request_data['transaction_id'],
            self.request_data['out_refund_no'],
            self.request_data['out_trade_no'],
            self.request_data['refund_id']
        ]
        count = 0
        for arg in metex_args:
            if arg:
                count += 1
            if count > 1:
                raise TooManyArgumentError(
                    "You can only choose one from 'transaction_id','out_refund_no','out_trade_no', 'refund_id"
                )


class PaymentNotification(BaseNotification):
    def __init__(self, data, **kwargs):
        super(PaymentNotification, self).__init__(data, **kwargs)


class RefundNotification(BaseNotification):
    """process refund notification process class"""
    def __init__(self, data, **kwargs):
        super(RefundNotification, self).__init__(data, **kwargs)

    def decrypt(self):
        """
         base64 decoding the encrypted string req_info to get b,
         md5 encoding b to get md5_key
        """
        b = base64.b64decode(self.response_data.get('req_info').encode('utf-8'))
        md5_key = md5(self.config['key'].encode('utf-8')).hexdigest()

        aes = AES.new(md5_key.encode('utf-8'), AES.MODE_ECB)
        encrypted_text = aes.decrypt(b)
        pattern = re.compile('<root>.*</root>', flags=re.S)
        encrypted_text = pattern.match(encrypted_text.decode('utf-8')).group()
        encrypted_dict = BaseMiniPay.xml_to_dict(encrypted_text, root='root')
        for k, v in encrypted_dict.items():
            self.response_data[k] = v
        self.response_data.pop('req_info')

    def _decision_rules(self):
        self.decrypt()

