from django.shortcuts import render,HttpResponseRedirect
from Store.models import *
from Qshop.views import setPassword,loginValid_store
@loginValid_store
def index(request):
    # return HttpResponse("this is Store`s views")
    return render(request,"store/base.html")

# def login(request):
#     if request.method =="POST" and request.POST:
#         username=request.POST.get("username")
#         password = request.POST.get("password")
#         store = Store.objects.filter(login_name=username).first()
#         if store:
#             form_password = setPassword(password)
#             db_password = store.password
#             if form_password == db_password:
#                 response=HttpResponseRedirect("/Store/index/")
#                 response.set_cookie("username",store.login_name)
#                 return response
#     return render(request,"store/login.html")
def login(request):
    if request.method == "POST" and request.POST:
        username = request.POST.get("username")
        password= request.POST.get("password")
        store = Store.objects.filter(login_name=username).first()
        if store:
            form_password = setPassword(password)
            db_password=store.password
            if form_password == db_password:
                response = HttpResponseRedirect("/Store/index/")
                response.set_cookie("username",store.login_name)
                return response
    return render(request,"store/login.html")



#注册
def register(request):
    if request.method == "POST" and request.POST:
        data = request.POST
        img = request.FILES.get("logo")
        store = Store()
        store.store_name = data.get("store_name")
        store.login_name = data.get("username")
        store.password = setPassword(data.get("password"))
        store.email = data.get("email")
        store.phone = data.get("phone")
        store.address = data.get("address")
        store.address = data.get("address")
        store.logo = img
        store.save()
        return HttpResponseRedirect("/Store/login/")
    return render(request,"store/register.html")

#退出登录
def logout(request):
    response=HttpResponseRedirect("/Store/login/")
    response.delete_cookie("username")
    return response

def addCommodity(request):
    types = Type.objects.all()
    if request.method == "POST":
        data = request.POST
        name = data.get("name")
        price = data.get("price")
        number = data.get("number")
        datas = data.get("data")
        safe = data.get("safe")
        address = data.get("address")
        types = data.get("types")
        picture = request.FILES.get("picture")
        content = data.get("content")

        c = Commodity()
        c.commodity_name = name
        c.commodity_id = "20190102"
        c.commodity_price=price
        c.commodity_number= number
        c.commodity_picture=picture
        c.commodity_data = datas
        c.commodity_safe_data=safe
        c.commodity_address= address
        c.delete_flage="false"
        c.commodity_content=content
        c.type = Type.objects.get(id=int(types))#添加外键
        # c.save()
        #添加多对多关系
        store_login_name = request.COOKIES.get("username")#通过cookie获取的店铺登陆名称
        # store = Store.objects.get(login_name=store_login_name) #通过登陆名获取商店数据
        c.shop=Store.objects.get(login_name=store_login_name)#添加数据到商品中
        c.save() #保存
        return HttpResponseRedirect("/Store/listCom/up/1")
    return render(request,"store/addCommodity.html",locals())

from django.core.paginator import Paginator
def listCommodity(request,type,page):
    page_int = int(page)
    if type == "down":
        commodity_list = Commodity.objects.filter(delete_flage="true").order_by("-commodity_data")
    else:
        commodity_list = Commodity.objects.filter(delete_flage="false").order_by("commodity_data")
    print(commodity_list)
    paginator = Paginator(commodity_list,10,orphans=0)

    index_all=len(commodity_list)-1
    index_count=int(index_all/10)+1
    # print(index_count)

    page = paginator.page(page_int)
    if index_count<5:
        page_range = range(1,index_count)
    else:
        if page_int < 4:
            page_range = range(1,6)
        elif page_int<index_count-2:
            page_range = paginator.page_range[page_int-3:page_int+2]
        else:
            page_range=range(index_count-4,index_count+1)
    return render(request,"store/listCommodity.html",{"page_data":page,"page_range":page_range,"type":type,"index_count":index_count})


def soldCommodity(request,type,id):
    referer = request.META.get("HTTP_REFERER")
    commodity = Commodity.objects.get(id = int(id))
    if type == "up":
        commodity.delete_flage="false"
    else:
        commodity.delete_flage="true"
    commodity.save()
    return HttpResponseRedirect(referer)

def deleteCommodity(request,id):
    referer = request.META.get("HTTP_REFERER")
    commodity = Commodity.objects.get(id = int(id))
    commodity.delete()
    return HttpResponseRedirect(referer)

def listType(request,page):
    page_int=int(page)
    type_list=Type.objects.all().order_by("parent")
    paginator = Paginator(type_list,10)
    page=paginator.page(page_int)
    if page_int<4:
        page_range=range(1,6)
    else:
        page_range=paginator.page_range[page_int-3,page_int+2]
    return render(request,"store/listType.html",{"page_data":page,"page_range":page_range,"type":type})


def addType(request):
    Types = Type.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        types = request.POST.get("types")
        picture = request.FILES.get("picture")

        t=Type()
        t.name = name
        t.parent = types
        t.picture = picture
        t.save()
    return render(request,"store/addType.html",locals())

def deleteType(request,id):
    refere = request.META.get("HTTP_REFERER")
    type=Type.objects.get(id=(int(id)))
    type.delete()
    return HttpResponseRedirect(refere)


from django.http import HttpResponse
import random
def addData(request):
    #types=["海产","肉类","粮油","蛋奶","水果","海外"]
    # for i in types:
    #     ty =Type()
    #     ty.name = i
    #     ty.parent=0
    #     ty.save()
    commodity = ["冷冻饺子","冷冻汤圆","冷冻果冻","冰激凌","雪糕","冰棒","冰西瓜"]
    country = "美国、加拿大、澳大利亚、德国、法国、英国、中国、新西兰、日本、以色列、印度、马来西亚、丹麦、荷兰、越南、巴西、埃及、俄罗斯".split("、")
    for i in range(50):
        com = Commodity()
        c = random.choice(country)
        com.commodity_name =c + random.choice(commodity)
        com.commodity_id = str(i).zfill(9)
        com.commodity_price = random.randint(13,190)
        com.commodity_number=random.randint(50,3000)
        com.commodity_data = "%s-%s-%s"%(2019,random.randint(1,5),random.randint(1,28))
        com.commodity_safe_data = 120
        com.commodity_address = c
        com.commodity_content = "冰凉一夏"

        com.delete_flage="false"
        com.type = Type.objects.get(id =12 )#random.randint(21,22)


        b=Store.objects.get(login_name="luoluo100")
        com.shop=b

        com.save()

    return HttpResponse("保存成功")
# Create your views here.

def order_list(request):
    #查询所有商品
    store=Store.objects.get(login_name=request.COOKIES.get("username"))
    order_list = store.orderresource_set.all()
    return render(request,"store/order_list.html",locals())
























