# Generated by Django 2.2.7 on 2019-11-25 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chongzhi', '0013_taocan_shangpin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='kami',
            field=models.CharField(max_length=32, verbose_name='卡密'),
        ),
    ]
