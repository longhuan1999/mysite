# Generated by Django 2.2.7 on 2019-11-17 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chongzhi', '0006_auto_20191117_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='beizhu',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='备注'),
        ),
    ]