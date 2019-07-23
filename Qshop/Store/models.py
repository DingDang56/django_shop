from django.db import models

# Create your models here.
class Type(models.Model):
    name=models.CharField(max_length=32)
    parent = models.IntegerField()
    picture = models.ImageField(upload_to="store/images",default="store/images/fenghuang.png")

    def __str__(self):
        return self.name


class Store(models.Model):
    store_name=models.CharField(max_length=32)
    login_name=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
    email=models.EmailField()
    phone=models.CharField(max_length=32)
    address=models.CharField(max_length=32)
    logo=models.ImageField(upload_to="store/images")

    def __str__(self):
        return self.store_name


class Commodity(models.Model):
    commodity_name=models.CharField(max_length=32)
    commodity_id = models.CharField(max_length=32)
    commodity_price = models.FloatField()
    commodity_number = models.IntegerField()
    commodity_picture = models.ImageField(upload_to="store/images")
    commodity_data = models.DateField()
    commodity_safe_data = models.IntegerField()
    commodity_address = models.TextField()
    commodity_content = models.TextField()

    delete_flage=models.CharField(max_length=32,default="false")
    type = models.ForeignKey(to=Type,on_delete=True)
    shop = models.ForeignKey(to= Store,on_delete=True)#manytomany会报错


class Picture(models.Model):
    image=models.ImageField(upload_to="store/images")
    commodity = models.ForeignKey(to=Commodity,on_delete=True)