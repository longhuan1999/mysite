# Generated by Django 2.2.7 on 2019-11-16 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chongzhi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='qr_url',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='二维码'),
        ),
    ]
