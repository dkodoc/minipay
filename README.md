# Minipay 

## 配置
配置参数存放在minipay包下的config.py文件中，配置选项有以下：

### APP_ID

小程序的appid

### MCH_ID

商户mch_id

### SECRET

小程序secret

### NONCE_STR

小程序nonce_str

### KEY

小程序key

### PAYMENT_NOTIFY_URL

支付通知回调接口

### REFUND_NOTIFY_URL

退款通知回调接口

### DEFAULT_MODE

默认的模式: ignore 不保存记录; store 保存记录，但是需要传入model值

### DEFAULT_METHOD

默认的请求方法：get 或者 post

### API_UNIFIED_ORDER

微信小程序统一下单接口

### API_ORDER_QUERY

微信小程序订单查询接口

### API_CLOSE_ORDER

微信小程序关闭订单接口

### API_REFUND

微信小程序申请退款接口

### API_REFUND_QUERY

微信小程序退款查询接口



## 接口方法

#### 统一下单

```python
import minipay
# from minipay import UnifiedOrder
minipay.UnifiedOrder()
```



### 订单查询

```python
import minipay
minipay.OrderQuery()
```

### 关闭订单

```python
import minipay
minipay.CloseOrder()
```

### 申请退款

```python
import minipay
minipay.Refund()
```

### 查询退款

```python
import minipay
minipay.RefundQuery()
```

### 支付通知处理

```python
import minipay
minipay.PaymentNotification()
```

### 退款通知处理

```python
import minipay
minipay.RefundNotification()
```





## 使用示例

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

