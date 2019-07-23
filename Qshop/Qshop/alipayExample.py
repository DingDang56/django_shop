from alipay import AliPay

alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1PVEc5cQD0IR5U1fFBxI3LW47yYqFOMX4QC2GWhCz1EekcGXsB4Eh4D7E1uJ8p+8r+5SoiPmXW/wI6sjMfdtO26QKpQWrs/s0TVLaCDV8/IgxV0vMwXdgsX8hx3jPrXnDdXh6xh7+mZkIoYmAGTQMsQ3vIzkoJFtu/TkMZG46Xvb0Y0VsiS4KnfklVNOeojsPuzspjY9MyFuXiIXZ7Kr0ovHPRVqdwIEoSdhfvSOrkYYKKA994c283OdcwgsVlxGnyRI6M4OzaKL+vFad4twhQa2AhxcwePgxNq55Upcz/6ozSfnqEl9n13FOsWtT2Et3z/BhSl3pm8zO9Kw/81p2wIDAQAB
-----END PUBLIC KEY-----'''

app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
    MIIEogIBAAKCAQEA1PVEc5cQD0IR5U1fFBxI3LW47yYqFOMX4QC2GWhCz1EekcGXsB4Eh4D7E1uJ8p+8r+5SoiPmXW/wI6sjMfdtO26QKpQWrs/s0TVLaCDV8/IgxV0vMwXdgsX8hx3jPrXnDdXh6xh7+mZkIoYmAGTQMsQ3vIzkoJFtu/TkMZG46Xvb0Y0VsiS4KnfklVNOeojsPuzspjY9MyFuXiIXZ7Kr0ovHPRVqdwIEoSdhfvSOrkYYKKA994c283OdcwgsVlxGnyRI6M4OzaKL+vFad4twhQa2AhxcwePgxNq55Upcz/6ozSfnqEl9n13FOsWtT2Et3z/BhSl3pm8zO9Kw/81p2wIDAQABAoIBAH4TIk5IXZKa69tT3fka8avwzaaPcpRhCY8Ei8oo5ny0KqPh97qlWssZ+gqww89m8B87uaISHNyuW33SYIjBUeLAhwseFvuxTyNgKN9hqSi97NbLXxkW3NgB/InFkPZcXIjdWd2D5koM+jVSNAdBp9yWO+UdiHDjCBMhXUNXYSCgRZLg9cWxf+C8ZlgVKGzYwocq8v18NsCvD7CykqI4wZ/LPh5waaDXxeb39zoLPV6B2IwWrRpN7gFS7fu75nbglhcEKaJ/eYTJY1bw4zABaSGSL7tFI4Cn2K4kH7cEr1iidxJqzs92E1YaC+KS4zaX9iq3WmCs/FNgdBa5PI7cIkECgYEA8h5a+BTz4BYR6i3t4+rhokj0eBHEG7+ngcRGE9/hkg45A/BGLeSCOJPrNl332TTUhEjQB89JkeA70SMtGGVLi97tJ+aqdzqJfbYdiJ241PNO614vd9wfBUY4n0qpVNu9vQlHMZKFQbETz+mJJdmZEf/BXYaGgo0Ph1WrujzqgmECgYEA4SrqN+jm/NfA2MUol29STzTwkdHfdAHdWvFZPmMTchXlhnKiCgQQLbZF2LtLRRPJAkEj+tjQA+USO6hAW4hYsE1T0d91akUwIpUPFUVjQCH7xRaboiH0YaCv9f18YEz5Ftuw7tBULFTrgaX9mrkv0cxWAnKzk/qq5mjuYG3pTbsCgYBdqtSyqRh4FtGzcTVZOWM1L1g0o1rlCU46a75YrgJMSOhR18CuvHqMfN1AWTYrd77HtouUmeLyZnd9v0gQ6g9B+2pwR1KncaQDWFMwqSP6bm6XrAZdLnFpzvLU3UOJKsHKwi4ixXZ8JY9ungCK/hWz2ufp0MN0+jGJv+EB2dM3wQKBgAVwUu38yy+KSpcx0/QsdTGCltj+18XmkaEzuTMfk4Wq77tao31YcceY4oEErSHDA5TxW9wgRo4Bh3o3ay6K0ZGYnJCyNBTYDPyY2x9paKdQ6tLs4997sHp3Nijb8Zgl49JghhqOn6nedz3Pc5u8I2KO6/jtKldFs8ETAccEgKEnAoGAekKsD069pplA+Wjm6ONewSFgho3jCVu7SqUIhw161l6AN74OjyvU0TIdLWJ9c1Ysb9jmcYr2VgY7weuaNdcLFHnsq1Q8Vb+YfYicJb67qhL2GvUuUn0s8jlrb7staF2Fala29mGkjoj77d+fPqKv0oyO/t/vGwyhJpRm7/RSK/4=
-----END RSA PRIVATE KEY-----'''

# 如果在Linux下，我们可以采用AliPay方法的app_private_key_path和alipay_public_key_path方法直接读取.emp文件来完成签证
# 在windows下，默认生成的txt文件，会有两个问题
# 1、格式不标准
# 2、编码不正确 windows 默认编码是gbk

# 实例化应用
alipay = AliPay(
    appid="2016093000628367",  # 支付宝app的id
    app_notify_url=None,  # 回调视图
    app_private_key_string=app_private_key_string,  # 私钥字符
    alipay_public_key_string=alipay_public_key_string,  # 公钥字符
    sign_type="RSA2",  # 加密方法
)
# 发起支付
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="3345416", #订单号
    total_amount=str(2000),  # 将Decimal类型转换为字符串交给支付宝
    subject="商贸商城",
    return_url=None,
    notify_url=None  # 可选, 不填则使用默认notify url
)
# 让用户进行支付的支付宝页面网址
print("https://openapi.alipaydev.com/gateway.do?" + order_string)
