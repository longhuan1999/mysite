# Generated by Django 2.2.7 on 2019-11-17 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chongzhi', '0004_order_sessionid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='sessionid',
        ),
        migrations.AddField(
            model_name='order',
            name='csrftoken',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='用户cookie'),
        ),
    ]
