# Generated by Django 3.0.3 on 2020-11-08 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chongzhi', '0018_auto_20201108_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kami',
            name='use',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='卡密状态'),
        ),
    ]