# Minipay 

python版本: python3
#### 1. 安装依赖
> 切换到项目根目录
```python
pip install -r requirements.txt
```
> API
```python
import minipay

# 统一下单
unified = minipay.UnifiedOrder()

# 成功时，response为微信响应的数据，否则为unified.error
# unified.error包含两个键，分别是 'code' and 'desc'，他们的值从响应中提取
response = unified.request()

# 查询业务是否成功
print(unified.is_success)
# 查询业务是否失败
print(unified.is_fail)
# 查询错误信息
print(unified.error)

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


# 申请退款
# 使用这个来退款，用法都是一样的
# 它有一些必须参数
refund_fee = 10
total_fee = 20
refund = minipay.Refund(
    out_trade_no=out_trade_no,
    total_fee=total_fee,
    refund_fee=refund_fee
    )
response = refund.request()
...

# 退款查询
minipay.RefundQuery()

# 支付通知处理
# 微信发过来的是XML格式的数据，直接丢进类里面处理即可
# django 示例
from django.http import HttpResponse
from models.models import PayNotice
def payment_notification(request):
    notice = minipay.PaymentNotification(
    data=request.body,
    model=PayNotice,
    mode='store'
    )
    # response 是用来返回给微信的信息，一个XML格式的数据
    response = notice.handle()
    return HttpResponse(response, content_type='application/xml')
    
#退款通知
# 用法和支付通知一样
minipay.RefundNotification()

```
将<b>minipay</b>目录下的<b>minipay</b>包复制到你的项目中即可。
#### 2. 使用示例
```python
import minipay

# 统一下单
# 必传参数
# out_trade_no
# openid
# body
# total_fee
unified = minipay.UnifiedOrder(
    out_trade_no=123123132,
    openid='mock openid',
    body='商品描述',
    total_fee=100
)
# 发起请求
response = unified.request()
# 根据 is_fail 或 is_success 判断业务是否成功
# unified.request()会返回一个响应
# if is fail,返回的是unified.error
# if is success,返回的是unified.response_data
# 不管是unified.error 还是unified.response_data
# 都是一个dict类型,其中unified.response_data包含了微信小程序返回的所有参数

if unified.is_fail:
    print(unified.error['code'], unified.error['desc'])
    print(response.get('code'), response.get('desc'))
elif unified.is_success:
    print(unified.response_data)
    print(response)


data = dict(out_trade_no=123123132,openid='mock openid',body='商品描述',total_fee=100)

unified = minipay.UnifiedOrder(**data)
response = unified.request()
if unified.is_fail:
    print(unified.error['code'], unified.error['desc'])
else:
    print(unified.response_data)
```

