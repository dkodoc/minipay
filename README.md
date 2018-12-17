# Minipay 

python版本: python3
#### 1. 安装依赖
> 切换到项目根目录
```bash
pip install -r requirements.txt
```
> config.py配置，使用前请配置minipay/config.py文件
```python
APP_ID = None # 小程序appid
MCH_ID = None # 商家mch_id
SECRET = None # 小程序secret
NONCE_STR = None # 小程序随机字符串
KEY = None # 小程序key，用于解密微信退款通知发来的加密字符串

# 支付通知和退款通知回调接口，根据自己的后台接口填写
# 比如 https://www.xxxx.com/api/payment/notice
PAYMENT_NOTIFY_URL = None
REFUND_NOTIFY_URL = None


# 微信退款需要用到的商户证书，没有配置的话请求退款会出错
# 详情见：https://pay.weixin.qq.com/wiki/doc/api/wxa/wxa_api.php?chapter=4_3
# 例如
# CERT = '/appclient.pem'
# CERT_KEY = '/appclient_key.pem'
CERT = ''
CERT_KEY = ''

# 默认模式， 目前有 ignore 和 store， store则必须提供ORM模型类用来保存请求和响应记录, ignore模式不保存记录
DEFAULT_MODE = 'ignore'

# 默认的ORM模型类，可以到用的时候再填
DEFAULT_MODEL = None

# 默认请求方法 post or get
DEFAULT_METHOD = 'post'

# 如果微信接口不更新，下面的不用更改
API_UNIFIED_ORDER = "https://api.mch.weixin.qq.com/pay/unifiedorder"
API_ORDER_QUERY = "https://api.mch.weixin.qq.com/pay/orderquery"
API_CLOSE_ORDER = "https://api.mch.weixin.qq.com/pay/closeorder"
API_REFUND = "https://api.mch.weixin.qq.com/secapi/pay/refund"
API_REFUND_QUERY = "https://api.mch.weixin.qq.com/pay/refundquery"
```
> API
#### 统一下单
```python
import minipay

# 以下三个为必传参数
data = {
    "out_trade_no": "2018112312321321",
    "body": "XX公司-珍珠奶茶",
    "total_fee": "700", # 这里单位是（分） 200=2元
}
unified = minipay.UnifiedOrder(**data)

# 如果请求成功，result为微信响应原始内容，否则为一个字典，包含微信返回的错误码和错误说明：
# {"code": "错误码", "desc": "错误说明"}
result = unified.request()
# unidfied有is_success和is_fail方法，用来判断请求是否成功
if unified.is_success:
    print("请求成功")
else:
    print(result.get("code"))
    print(result.get("desc"))

# 错误也可以通过unified.error属性获得
print(unified.error)
```
#### 订单查询
```python
import minipay
# 订单查询
# 使用这个接口，你可以很方便的查询在你小程序下的所有订单
# 调用的方法只需要输入订单号

out_trade_no = 'abv2010102333112'
query = minipay.OrderQuery(out_trade_no=out_trade_no)
response = query.request()
if query.is_success:
    print(response)
    print(query.response_data)
else:
    print(query.error)
    print(response)
```
#### 关闭订单
```python
import minipay

close_order = minipay.CloseOrder(out_trade_no="abv2010102333112")
close_order.request()
if close_order.is_success:
    print(close_order.response_data)
else:
    print(close_order.error)

```
#### 申请退款
```python
# 申请退款
# 使用这个来退款，用法都是一样的
# 它有一些必须参数
import minipay


refund_fee = 10
total_fee = 20
refund = minipay.Refund(
    out_trade_no="12313123",
    total_fee=total_fee,
    refund_fee=refund_fee
    )
response = refund.request(cert=(refund.config["cert"], refund.config["cert_key"]))
if refund.is_success:
    pass
else:
    pass

```
#### 退款查询
```python
import minipay

# out_trade_no，out_refund_no，transaction_id三选1
query = minipay.RefundQuery(out_trade_no="asdasd")
query.request()
if query.is_success:
    pass
else:
    pass

```
#### 支付成功通知
```python
# 支付通知处理
# 微信发过来的是XML格式的数据，直接丢进类里面处理即可
# django 示例
from django.http import HttpResponse
from models.models import PayNotice

import minipay

def payment_notification(request):
    notice = minipay.PaymentNotification(
    data=request.body,
    model=PayNotice,
    mode='store'
    )
    # response 是用来返回给微信的信息，一个XML格式的数据
    response = notice.handle()
    return HttpResponse(response, content_type='application/xml')
```
#### 退款成功通知
```python
import minipay
from models.models import RefundNotice
from django.http import HttpResponse


def refund_notification(request):
    notice = minipay.RefundNotification(
        data=request.body,
        model=RefundNotice,
        mode='store',
    )
    response = notice.handle()
    return HttpResponse(response, content_type='application/xml')

```

将<b>minipay</b>目录下的<b>minipay</b>包复制到你的项目中即可。

