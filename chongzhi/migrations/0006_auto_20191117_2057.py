# Generated by Django 2.2.7 on 2019-11-17 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chongzhi', '0005_auto_20191117_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='csrftoken',
            field=models.CharField(default='frtyhujijyhtgrr456787uer45t67ujy', max_length=100, verbose_name='用户cookie'),
            preserve_default=False,
        ),
    ]