# Generated by Django 2.2.1 on 2019-05-23 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0003_orderresource_small_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='receive',
            field=models.CharField(default='Null', max_length=32),
        ),
    ]
