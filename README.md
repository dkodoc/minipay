# minipay
## 
### 配置config.py
> APP_ID

小程序的appid
> MCH_ID

商户mch_id
> SECRET

小程序secret
> NONCE_STR

小程序nonce_str
> KEY

小程序key
> PAYMENT_NOTIFY_URL

支付通知回调接口
> REFUND_NOTIFY_URL

退款通知回调接口
> DEFAULT_MODE

默认的模式: ignore 不保存记录; store 保存记录，但是需要传入model值
> DEFAULT_METHOD

默认的请求方法：get 或者 post
> API_UNIFIED_ORDER

微信小程序统一下单接口
> API_ORDER_QUERY

微信小程序订单查询接口
> API_CLOSE_ORDER

微信小程序关闭订单接口
> API_REFUND

微信小程序申请退款接口
> API_REFUND_QUERY

微信小程序退款查询接口


### 使用示例
```python
import minipay

unified = minipay.UnifiedOrder(
                out_trade_no=123123132,
                openid='mock openid',
                body='商品描述',
                total_fee=100
                )
response = unified.request()
if unified.is_fail:
    print(unified.error['code'], unified.error['desc'])
else:
    print(unified.response_data)


data = dict(out_trade_no=123123132,openid='mock openid',body='商品描述',total_fee=100)

unified = minipay.UnifiedOrder(**data)
response = unified.request()
if unified.is_fail:
    print(unified.error['code'], unified.error['desc'])
else:
    print(unified.response_data)
```

