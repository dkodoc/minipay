from hashlib import md5
from xml.dom import minidom
import xml.etree.ElementTree

import requests
from minipay.config import MiniAppsConfig
from minipay.exceptions import ModelError, ModeError, TargetError, MethodError

__all__ = ['BaseMiniPay', 'BaseNotification']


class BaseMiniPay(object):
    def __init__(self, **kwargs):
        self.config = {
            'app_id': None, 'mch_id': None, 'secret': None, 'nonce_str': None,
            'key': None, 'cert': None, 'cert_key': None, 'payment_notify_url': None,
            'refund_notify_url': None, 'default_mode': None, 'default_model': None,
            'default_method': None, 'api_unified_order': None, 'api_order_query': None,
            'api_close_order': None, 'api_refund': None, 'api_refund_query': None
        }
        self.target = None
        self.notify_url = None
        self.method = kwargs.get("method")
        self.request_data = dict()
        self.response_data = dict()
        self.error = dict()
        self.options = dict()
        self.model = kwargs.get('model')
        self.mode = kwargs.get('mode')
        self.initialize()

    def initialize(self):
        self.method = self.config['default_method']
        self.mode = self.config['default_mode']

    def config_from_object(self, config_obj):
        for attr, value in config_obj.__dict__.items():
            if attr.startswith('_'):
                continue
            lowed_attr = attr.lower()
            if lowed_attr in self.config.keys():
                self.config[lowed_attr] = value
        self.initialize()

    def _decision_rules(self):
        pass

    def request(self):
        self._decision_rules()
        self._filter(self.request_data)
        self.sign()
        request_data_xml = self.dict_to_xml(self.request_data)

        if self.target is None:
            raise TargetError("object's target attribute must be a url.")
        if self.method == 'post':
            resp_xml = requests.post(self.target, request_data_xml, **self.options)
        elif self.method == 'get':
            resp_xml = requests.get(self.target, request_data_xml, **self.options)
        else:
            raise MethodError("object's method attribute must be 'post' or 'get'.")

        resp_xml.encoding = 'utf-8'
        self.response_data = self.xml_to_dict(resp_xml.text)

        if self.mode == 'store':
            try:
                self._store()
            except (ModelError, ModeError) as err:
                print(err)
        return self._handle_response()

    def _handle_response(self):
        if self.request_is_successfully:
            if self.business_is_successfully:
                return self._handle_successful_business()
            else:
                return self._handle_failing_business()
        else:
            return self._handle_failing_request()

    def _handle_successful_business(self):
        return self.response_data

    def _handle_failing_business(self):
        self.error['code'] = self.response_data['err_code']
        self.error['desc'] = self.response_data['err_code_des']
        return self.error

    def _handle_failing_request(self):
        self.error['code'] = self.response_data['return_code']
        self.error['desc'] = self.response_data['return_msg']
        return self.error

    @property
    def is_success(self):
        return self.request_is_successfully and self.business_is_successfully

    @property
    def is_fail(self):
        return not self.request_is_successfully or not self.business_is_successfully

    @property
    def request_is_successfully(self):
        return 'SUCCESS' == self.response_data.get('return_code')

    @property
    def business_is_successfully(self):
        return 'SUCCESS' == self.response_data.get('result_code')

    @staticmethod
    def dict_to_xml(data):
        if not isinstance(data, dict):
            raise TypeError("data object must be a dict type.")

        dom = minidom.Document()
        root = dom.createElement('xml')
        dom.appendChild(root)
        for key, value in data.items():
            sub_node = dom.createElement(key)
            root.appendChild(sub_node)
            text = dom.createTextNode(str(value))
            sub_node.appendChild(text)

        return dom.toprettyxml(encoding='utf-8')

    @staticmethod
    def xml_to_dict(data, root='xml'):
        """
        传入一个xml字符串， 返回一个字典类型的对象.
        root可以规定xml的根名称，此方法会对根节点进行忽略
        """
        d = {}
        elements = xml.etree.ElementTree.fromstring(data)
        for element in elements.iter():
            if element.tag == root:
                continue
            d[element.tag] = element.text
        return d

    def _filter(self, data):
        for key, value in data.items():
            if key in self.request_data.keys():
                self.request_data[key] = value

        filtered_data = {}
        for key, value in self.request_data.items():
            if value and value != "":
                filtered_data[key] = value
        self.request_data = filtered_data

    def sign(self, data=None):
        if data is None:
            data = self.request_data

        if not isinstance(data, dict):
            raise TypeError("")

        formatted = ''
        for key in list(sorted(data.keys())):
            string = key + '=' + str(data.get(key)) + '&'
            formatted += string

        formatted += 'key=%s' % self.config['key']
        sign = md5(formatted.encode())
        sign = sign.hexdigest().upper()
        self.request_data['sign'] = sign
        return sign

    def _store(self):
        if self.mode == 'ignore':
            raise ModeError("Current mode is 'ignore', that can't be store the request data or response data.")
        if self.model is None:
            raise ModelError('%s model attribute does not set.' % self.__class__.__name__)
        if self.mode == 'store':
            new_record = self.model()
            for attr, value in self.response_data.items():
                if hasattr(new_record, attr):
                    setattr(new_record, attr, value)
            for attr, value in self.request_data.items():
                if hasattr(new_record, attr):
                    setattr(new_record, attr, value)
            new_record.save()


class BaseNotification(object):
    def __init__(self, data, **kwargs):
        data = BaseMiniPay.xml_to_dict(data)
        self.response_data = data
        self.config = {
            'key': MiniAppsConfig.KEY,
            'mode': kwargs.get('mode') or MiniAppsConfig.DEFAULT_MODE,
        }
        self.mode = kwargs.get('mode') or self.config['mode']
        self.model = kwargs.get('model')

    def sign(self, data=None):
        if data is None:
            data = self.response_data

        if not isinstance(data, dict):
            raise TypeError("")

        formatted = ''
        for key in list(sorted(data.keys())):
            string = key + '=' + str(data.get(key)) + '&'
            formatted += string

        formatted += 'key=%s' % self.config['key']
        sign = md5(formatted.encode())
        sign = sign.hexdigest().upper()
        return sign

    def _verifysign(self):
        serversign = self.response_data.pop('sign')
        localsign = self.sign()
        if serversign == localsign:
            return True
        return False

    def _verify_fee(self):
        if self.model is None:
            return True
        return False

    def decrypt(self):
        pass

    def _decision_rules(self):
        pass

    def handle(self):
        if self.is_finish:
            return self._successful_formatted()

        if self._verifysign():
            self._store()
            return self._successful_formatted()
        return self._failing_formatted('sign invaild.')

    @staticmethod
    def _successful_formatted(text=None):
        response = {
            'return_code': 'SUCCESS',
            'return_msg': text or 'OK'
        }
        return BaseMiniPay.dict_to_xml(response)

    @staticmethod
    def _failing_formatted(text=None):
        response = {
            'return_code': 'FAIL',
            'return_msg': text or 'FAIL'
        }
        return BaseMiniPay.dict_to_xml(response)

    def _store(self):
        if self.mode == 'ignore':
            raise ModeError("Current mode is 'ignore', that can't be store the request data or response data.")
        if self.model is None:
            raise ModelError('%s model attribute does not set.' % self.__class__.__name__)
        if self.mode == 'store':
            new_record = self.model()
            for attr, value in self.response_data.items():
                if hasattr(new_record, attr):
                    setattr(new_record, attr, value)
            new_record.save()

    @property
    def is_finish(self):
        if self.model is None:
            return False
        return True
