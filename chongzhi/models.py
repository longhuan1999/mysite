from django.db import models
import datetime
from django.utils import timezone
# Create your models here.


class Shangpin(models.Model):
    shangpin = models.CharField(max_length=18, verbose_name='商品', primary_key=True)

    class Meta:
        db_table = 'tb_shangpin'
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.shangpin


class Kami(models.Model):
    kami = models.CharField(unique=True, max_length=32, verbose_name='卡密')
    taocan = models.ForeignKey("Taocan", on_delete=models.PROTECT)
    use = models.PositiveSmallIntegerField(default=0, verbose_name='卡密状态')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    last_save = models.DateTimeField(auto_now=True, verbose_name='修改日期')

    class Meta:
        db_table = 'tb_kami'
        verbose_name = '卡密'
        verbose_name_plural = verbose_name

    def __str__(self):
        #return self.kami
        return self.kami


class Taocan(models.Model):
    taocan = models.CharField(max_length=18, verbose_name='套餐', primary_key=True)
    shangpin = models.ForeignKey("Shangpin", on_delete=models.PROTECT)
    alipay_price = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='支付宝价格')
    wechat_price = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='微信价格')

    class Meta:
        db_table = 'tb_taocan'
        verbose_name = '套餐'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.taocan


class Order(models.Model):
    order_id = models.AutoField(primary_key=True, verbose_name='订单号')
    kami = models.CharField(max_length=32, verbose_name='卡密')
    order_name = models.CharField(max_length=18, verbose_name='商品名/套餐')
    order_status = models.CharField(max_length=8, verbose_name='订单状态')
    qr_price = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2, verbose_name='实付金额')
    order_type = models.CharField(max_length=6, verbose_name='支付方式')
    beizhu = models.CharField(null=True, blank=True, max_length=50, verbose_name='备注')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    last_save = models.DateTimeField(auto_now=True, verbose_name='修改日期')
    user_email = models.EmailField(verbose_name='买家邮箱')
    csrftoken = models.CharField(max_length=100, verbose_name="用户cookie")
    user_ip = models.CharField(null=True, blank=True, max_length=36, verbose_name='买家IP')
    qr_url = models.CharField(null=True, blank=True, max_length=200, verbose_name='二维码')

    class Meta:
        db_table = 'tb_order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_id)

    def was_guoqi(self):
        return self.add_date < timezone.now() - datetime.timedelta(minutes=5)
    
    def guoqi_time(self):
        guoqi_time = self.add_date + datetime.timedelta(minutes=5)
        return guoqi_time


class APP_POST(models.Model):
    money = models.CharField(max_length=8, verbose_name='金额')
    encrypt = models.CharField(max_length=2, verbose_name='是否加密')
    time = models.CharField(max_length=20, verbose_name='时间')
    type = models.CharField(max_length=20, verbose_name='支付方式')
    title = models.CharField(max_length=15, verbose_name='标题')
    deviceid = models.CharField(max_length=100, verbose_name='设备号')
    content = models.CharField(max_length=100, verbose_name='详细内容')

    class Meta:
        db_table = 'tb_app_post'
        verbose_name = 'APP推送的收款信息'
        verbose_name_plural = verbose_name