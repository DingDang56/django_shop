from django.db import models
from Store.models import  *


# Create your models here.
class BuyUser(models.Model):
    login_name=models.CharField(max_length=32) #
    password=models.CharField(max_length=32) #
    username=models.CharField(max_length=32,blank=True,null=True)#
    email=models.EmailField(max_length=32)#
    phone = models.CharField(max_length=32,blank=True,null=True)#
    photo=models.ImageField(upload_to="buyer/images",blank=True,null=True)#


#购物车
class BuyCar(models.Model):
    commodity_name = models.CharField(max_length=32)#商品名称
    commodity_id = models.IntegerField()#商品ID
    commodity_price = models.FloatField()#商品价格
    commodity_number = models.IntegerField()#购买商品数量
    commodity_picture = models.ImageField(upload_to="static/images")#商品图片
    user_id = models.IntegerField()#用户id
    shop_id = models.IntegerField()#商店id


#收货地址
class Address(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=32)
    buyer_id = models.ForeignKey(to=BuyUser,on_delete=True)
    receive = models.CharField(max_length=32,default="未知")


#订单
class Order(models.Model):
    """
    待支付 0
    支付  1
    已发货 2
    确认收货    3
    """
    order_number = models.CharField(max_length=32)#订单编号
    user_address = models.ForeignKey(to=Address,on_delete=True)
    money = models.FloatField(blank=True,null=True)#金额
    state = models.IntegerField()#订单状态
    date = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(to=BuyUser,on_delete=True)


#订单总结
class OrderResource(models.Model):
    commodity_name=models.CharField(max_length=32)#商品名称
    commodity_id = models.IntegerField()#商品ID
    commodity_price = models.FloatField()#商品价格

    commodity_number = models.IntegerField()#购买商品数量
    commodity_picture = models.ImageField(upload_to="buyer/images")
    small_money = models.FloatField() #订单小计
    order_id = models.ForeignKey(to=Order,on_delete=True)#订单ID
    store_id = models.ForeignKey(to=Store,on_delete=True)#店铺ID