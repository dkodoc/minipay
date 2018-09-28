# coding: utf-8
from minipay.base import MiniPayBase


class UnifiedOrder(MiniPayBase):
    """"""
    def __init__(self, data={}, **kwargs):
        super(UnifiedOrder, self).__init__(data, **kwargs)
        self.target = data.get('target') or "https://api.mch.weixin.qq.com/pay/unifiedorder"
        self.notify_url = data.get('notify_url') or "https://www.duodongzhen.com/test/notifications/payment/"
        self.request_data = {
            'appid': self.config['app_id'],
            'mch_id': self.config['mch_id'],
            'device_info': None,
            'nonce_str': self.config['nonce_str'],
            'sign': None,
            'sign_type': None,
            'body': None,
            'detail': None,
            'attach': None,
            'out_trade_no': None,
            'fee_type': None,
            'total_fee': None,
            'spbill_create_ip': '47.94.162.104',
            'time_start': None,
            'time_expire': None,
            'goods_tag': None,
            'notify_url': self.notify_url,
            'trade_type': 'JSAPI',
            'limit_pay': None,
            'openid': None
        }

    def _handle_successful_business(self):
        pass

    def _handle_failing_business(self):
        pass

    def _handle_failing_request(self):
        pass


if __name__ == '__main__':
    data = {
        'total_fee': '11'
    }
    unified_order = UnifiedOrder(data)













