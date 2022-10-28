# Generated by Django 2.2.7 on 2019-11-25 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chongzhi', '0010_auto_20191119_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shangpin',
            fields=[
                ('shangpin', models.CharField(max_length=18, primary_key=True, serialize=False, verbose_name='商品')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'db_table': 'tb_shangpin',
            },
        ),
        migrations.AddField(
            model_name='taocan',
            name='shangpin',
            field=models.ForeignKey(default='xing', on_delete=django.db.models.deletion.PROTECT, to='chongzhi.Shangpin'),
            preserve_default=False,
        ),
    ]