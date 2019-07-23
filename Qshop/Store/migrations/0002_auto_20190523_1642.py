# Generated by Django 2.2.1 on 2019-05-23 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commodity',
            name='shop',
        ),
        migrations.AddField(
            model_name='commodity',
            name='shop',
            field=models.ForeignKey(default=1, on_delete=True, to='Store.Store'),
            preserve_default=False,
        ),
    ]
