# @Time    : 2019/5/20 9:32
# @Author  : 唐文杰
# @File    : urls.py
# @Software: PyCharm

from django.urls import path,re_path
from django.conf.urls import url
from Buyer.views import *
urlpatterns=[
    path("index/",index),
    re_path('list/(?P<type_id>\d+)/(?P<page>\d+)',shop_list),
    re_path('detail/(?P<com_id>\d+)',detail),
    path("register/",register),
    path('login/',login),
    path('cart/',cart),
    path('userCenter/',userCenter),
    path('userCenterOrder/',userCenterOrder),
    path('userCenterSite/',userCenterSite),
    path('place_order/',place_order),
    path('mobilephoneapp/',mobilephoneapp),
    # path("codeValid/",codeValid),
    # path('sendCode/',sendCode),
    path('Pay/',pay),
    re_path("rmcommodity/(\w+)",rmcommodity),
    url("^search$",search)
]