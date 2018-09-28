# coding: utf-8

from hashlib import md5
from xml.dom import minidom
import xml.etree.ElementTree
import requests
from minipay.config import MiniAppsConfig
from minipay.exceptions import *

__all__ = ['MiniPayBase']


class MiniPayBase(object):
    """
    mini-pay base class
    """

    def __init__(self, data={}, **kwargs):
        self.config = {
            'app_id': '',
            'mch_id': '',
            'secret': '',
            'nonce_str': '',
            'key': '',
        }
        self.config_from_object(MiniAppsConfig)
        self.target = None
        self.method = 'post'
        self.request_data = dict()
        self.response_data = dict()
        self.error = dict()
        self.model = None
        self.mode = 'ignore'

    def config_from_object(self, config_obj):
        for attr, value in config_obj.__dict__.items():
            if attr.startswith('_'):
                continue
            lowed_attr = attr.lower()
            if lowed_attr in self.config.keys():
                self.config[lowed_attr] = value

    def request(self):
        if self.target is None:
            raise TargetError("object's target attribute must be a url.")

        if self.method == 'post':
            resp_xml = requests.post(self.target, self.request_data)
        elif self.method == 'get':
            resp_xml = requests.get(self.target, self.request_data)
        else:
            raise MethodError("object's method attribute must be 'post' or 'get'.")

        resp_xml.encoding = 'utf-8'
        self.response_data = self.xml_to_dict(resp_xml.text)
        return self._handle_response()

    def _handle_response(self):
        """在子类的公有方法里面不允许调用此方法"""
        if self.request_is_successfully:
            if self.business_is_successfully:
                return self._handle_successful_business()
            else:
                return self._handle_failing_business()
        else:
            return self._handle_failing_request()

    def _handle_successful_business(self):
        """业务结果为成功时所执行的方法"""
        pass

    def _handle_failing_business(self):
        """业务结果为失败时所执行的方法"""
        pass

    def _handle_failing_request(self):
        """请求API失败时所执行的方法"""
        pass

    @property
    def request_is_successfully(self):
        return 'SUCCESS' == self.response_data['return_code']

    @property
    def business_is_successfully(self):
        return 'SUCCESS' == self.response_data['result_code']

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
            text = dom.createTextNode(value)
            sub_node.appendChild(text)

        return dom.toprettyxml(encoding='utf-8')

    @staticmethod
    def xml_to_dict(data):
        d = {}
        elements = xml.etree.ElementTree.fromstring(data)
        for element in elements.iter():
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
        print('dd', self.request_data)

    @staticmethod
    def _sign(self, data):
        """
        Wechat miniapps parameters sign.
        :param self:
        :param data: a dict
        :return: sign
        """
        if not isinstance(data, dict):
            raise TypeError("")

        formatted = ''
        for key in list(sorted(data.keys())):
            string = key + '=' + str(data.get(key)) + '&'
            formatted += string

        formatted += 'key=%s' % self.key
        sign = md5(formatted.encode())
        sign = sign.hexdigest().upper()
        return sign

    def _store(self):
        pass

