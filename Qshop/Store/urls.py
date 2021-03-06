# @Time    : 2019/5/20 9:37
# @Author  : 唐文杰
# @File    : urls.py
# @Software: PyCharm
from django.urls import path,re_path
from Store.views import *
urlpatterns = [
    path("index/",index),
    path("login/",login),
    path('register/',register),
    path('logout/',logout),
    path('addCom/',addCommodity),
    re_path('listCom/(?P<type>\w+)/(?P<page>\d+)/',listCommodity),
    re_path('soldCom/(?P<type>\w+)/(?P<id>\d+)/',soldCommodity),
    re_path('delete/(\d+)/',deleteCommodity),
    re_path('listType/(\d+)',listType),
    re_path('deleteType/(\d+)',deleteType),
    path('addType/',addType),
    path('order_list/',order_list),
]
urlpatterns +=[
    path("addData/",addData),
]