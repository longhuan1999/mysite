# Generated by Django 2.2.7 on 2019-11-19 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chongzhi', '0009_app_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kami',
            name='kami',
            field=models.CharField(max_length=18, unique=True, verbose_name='卡密'),
        ),
    ]