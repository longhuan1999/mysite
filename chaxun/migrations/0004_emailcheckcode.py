# Generated by Django 3.0.3 on 2020-11-09 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chaxun', '0003_auto_20191119_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailCheckCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('checkcode', models.CharField(max_length=18)),
                ('statu', models.PositiveSmallIntegerField(default=0, verbose_name='验证码状态')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('guoqi_data', models.DateTimeField(verbose_name='过期日期')),
            ],
            options={
                'verbose_name': '邮箱验证码',
                'verbose_name_plural': '邮箱验证码',
                'ordering': ['-add_date'],
            },
        ),
    ]
