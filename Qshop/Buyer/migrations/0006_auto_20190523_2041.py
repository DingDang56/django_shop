# Generated by Django 2.2.1 on 2019-05-23 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0005_auto_20190523_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='receive',
            field=models.CharField(default='未知', max_length=32),
        ),
    ]
