from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from Buyer.models import *
from Store.models import *
from Qshop.views import loginValid_buyer

@loginValid_buyer
def index(request):
    # return HttpResponse("this is Store`s index")
    # return render(request,"buyer/index.html")
    types = Type.objects.filter(parent = 0)
    name=BuyUser.objects.get(id=int(request.COOKIES.get("user_id")))
    # print(types)
    result = [
        # {"type":"粮油","data":["文莱牛排","缅甸大米","马来西亚牛肉","越南大米"]}
    ]
    for t in types:
        d = {}
        d["type"] = t
        d["data"] = t.commodity_set.filter(delete_flage="false").order_by("commodity_data")[:4]
        result.append(d)
    # print(result)
    return render(request,"buyer/index.html",locals())


#某类商品列表页
@loginValid_buyer
def shop_list(request,type_id,page):
    page_int=int(page)
    commoditys = Type.objects.get(id=int(type_id)).commodity_set.filter(delete_flage="false")
    # commoditys_price= Type.objects.get(id=int(type_id)).commodity_set.filter(delete_flage="false").order_by("commoditys_price")
    paginator = Paginator(commoditys,20)
    page = paginator.page(page_int)
    if page_int<4:
        page_range=range(1,6)
    else:
        page_range = paginator.page_range[page_int-3,page_int+2]
    if page == 1:
        previous_page=0
    else:
        previous_page = page_int-1
    next_page = page_int + 1
    result={
        'commoditys':page,#页面数据
        'page_range':page_range,#页码范围
        'type_id':type_id, #类型id
        'previous_page':previous_page,#上一页
        'next_page':next_page,#下一页
        }

    return render(request,'buyer/list.html',result)

@loginValid_buyer
def detail(request,com_id):
    commodity =Commodity.objects.get(id=int(com_id))
    if request.method=="POST":
        number = request.POST.get("number")
        car = BuyCar()
        car.commodity_name=commodity.commodity_name#商品名称
        car.commodity_id=commodity.id #商品id
        car.commodity_price=commodity.commodity_price
        car.commodity_picture=commodity.commodity_picture#商品图片

        car.commodity_number = int(number)#购买商品的数量
        id = commodity.shop.id
        car.shop_id=int(id)
        user_id = request.COOKIES.get("user_id")
        car.user_id = user_id #用户的id)
        car.save()
        return HttpResponseRedirect('/Buyer/cart')
    return render(request,"buyer/detail.html",locals())

from Qshop.views import setPassword
def register(request):
    if request.method=="POST":
        username=request.POST.get("user_name")
        password=request.POST.get("pwd")

        user = BuyUser()
        user.login_name=username
        user.password = setPassword(password)
        user.save()
        return HttpResponseRedirect('/')
    return render(request,'buyer/register.html')


def login(request):
    if request.method == "POST" and request.POST:
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        user = BuyUser.objects.filter(login_name=username).first()
        if user:
            db_password = user.password
            form_password = setPassword(password)
            if db_password == form_password:
                response = HttpResponseRedirect("/")
                response.set_cookie("username",user.login_name)
                response.set_cookie("user_id",user.id)
                return response
    return render(request,"buyer/login.html")

#购物车
def cart(request):
    user_id = int(request.COOKIES.get("user_id"))
    shop_list = BuyCar.objects.filter(user_id=user_id)
    shops = []
    for shop in shop_list:
        shops.append({
            "id":shop.id,
            "commodity_name":shop.commodity_name,
            "commodity_id":shop.id,
            "commodity_price":shop.commodity_price,
            "commodity_number":shop.commodity_number,
            "commodity_picture":shop.commodity_picture,
            "total":shop.commodity_price*shop.commodity_number,
        })
    return render(request,"buyer/carts.html",locals())

@loginValid_buyer
def userCenter(request):
    return render(request,"buyer/user_center.html")

@loginValid_buyer
def userCenterOrder(request):
    return render(request,"buyer/user_center_order.html")

@loginValid_buyer
def userCenterSite(request):
    add_list = Address.objects.all()
    # print(add_list)
    if request.method=="POST":
        receive = request.POST.get("receive")
        addr = request.POST.get("adress")
        phone = request.POST.get("phone")

        address = Address()
        address.address = addr
        address.receive = receive
        address.phone = phone
        address.buyer_id = BuyUser.objects.get(id=int(request.COOKIES.get("user_id")))
        address.save()
    return render(request,"buyer/user_center_site.html",locals())


from django.db.models import Q
def search(request):
    if request.method == "GET":
        getdate = request.GET
        des = getdate.get('search', None)
        error_msg = ""
        if not des:
            error_msg = '请输入商品名'
        commoditys = Commodity.objects.filter(Q(commodity_name__contains=des)&Q(delete_flage="false"))
        return render(request,"buyer/searchcommodity.html",locals())

def rmcommodity(request,id):
    referer = request.META.get("HTTP_REFERER")
    buy=BuyCar.objects.get(id=int(id))
    rmcommodity_id=buy.commodity_id
    try:
        OrderResource.objects.get(commodity_id=rmcommodity_id).delete()
    except Exception:
        pass

    BuyCar.objects.get(id=int(id)).delete()


    return HttpResponseRedirect(referer)

def place_order(request):
    if request.method == "POST":
        add_list = Address.objects.all()
        data = request.POST
        car_shop_list=[]
        for k,v in data.items():
            if v == "on":
                car_data = BuyCar.objects.get(id=int(k))
                car_shop_list.append(car_data)
        car_shop_list=enumerate(car_shop_list,1)
        return render(request,"buyer/place_order.html",locals())
    else:
        return HttpResponse("错误的请求方法")


def mobilephoneapp(request):
    return render(request,'buyer/mobilephoneapp.html')
# Create your views here.


#阿里支付
import datetime
from alipay import AliPay
def pay(request):
    if request.method=="GET" and request.GET:
        data = request.GET
        data_itme = data.items()
        order = Order()
        order.user_address=Address.objects.get(id=1)
        order.state = 0
        order.data = datetime.datetime.now()
        order.user_id = BuyUser.objects.get(id=int(request.COOKIES.get("user_id")))
        order.save()
        order.order_number = str(order.id).zfill(10)
        order.save()
        money=0
        for k,v in data_itme:
            if k.startswith("shop_"):
                car_id = int(v)
                data = BuyCar.objects.get(id=car_id)
                order_reource=OrderResource()
                order_reource.commodity_name=data.commodity_name
                order_reource.commodity_id=data.commodity_id
                order_reource.commodity_price=data.commodity_price
                order_reource.commodity_number=data.commodity_number
                order_reource.small_money=data.commodity_price*data.commodity_number
                order_reource.commodity_picture=data.commodity_picture
                # order_reource.store_id=Store.objects.get(id=1)
                order_reource.store_id=Store.objects.get(id=data.shop_id)
                order_reource.order_id=order
                order_reource.save()
                money += order_reource.small_money
        order.money = money
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
            out_trade_no=order.order_number,  # 订单号
            total_amount=str(order.money),  # 将Decimal类型转换为字符串交给支付宝
            subject="商贸商城",
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )
        # 让用户进行支付的支付宝页面网址
        return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)























