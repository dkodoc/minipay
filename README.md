# Minipay 

python版本: python3
#### 1. 安装依赖
> 切换到项目根目录
```python
pip install -r requirements.txt
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

