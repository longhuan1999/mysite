# Generated by Django 3.0.3 on 2020-11-09 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chaxun', '0004_emailcheckcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcheckcode',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
