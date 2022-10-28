
from django.db import models
from django.utils import timezone

class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"

class EmailCheckCode(models.Model):
    email = models.EmailField(unique=False)
    checkcode = models.CharField(max_length=18)
    statu = models.PositiveSmallIntegerField(default=0, verbose_name='验证码状态')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    guoqi_data = models.DateTimeField(verbose_name='过期日期')

    def __str__(self):
        return self.email

    def was_guoqi(self):
        return self.guoqi_data < timezone.now()

    class Meta:
        ordering = ["-add_date"]
        verbose_name = "邮箱验证码"
        verbose_name_plural = "邮箱验证码"