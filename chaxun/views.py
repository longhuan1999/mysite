import decimal
from django.urls import reverse
from django.utils import timezone
import datetime
import json
from django.shortcuts import render
from django.shortcuts import redirect
from .models import User, EmailCheckCode
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from chongzhi.models import Order, Kami
from .forms import UserForm, RegisterForm, EmailCheckForm, PasswdResetForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from functools import wraps
from urllib.parse import urlsplit
from requests import request
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
#from .hash_code import hash_code
#http = urlsplit(request.build_absolute_url(None)).scheme
#获得当前的HTTP或HTTPS
import dateutil.parser
 
CONVERTERS = {
    'datetime': dateutil.parser.parse,
    'decimal': decimal.Decimal,
}

class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime,)):
            return {"val": obj.isoformat(), "_spec_type": "datetime"}
        elif isinstance(obj, (decimal.Decimal,)):
            return {"val": str(obj), "_spec_type": "decimal"}
        else:
            return super().default(obj)
 
 
def object_hook(obj):
    _spec_type = obj.get('_spec_type')
    if not _spec_type:
        return obj
 
    if _spec_type in CONVERTERS:
        return CONVERTERS[_spec_type](obj['val'])
    else:
        raise Exception('Unknown {}'.format(_spec_type))


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)



@csrf_exempt
def index(request):
    if request.is_secure():
        http = "https"
    else:
        http = "http"
    host = request.META['HTTP_HOST']
    try:
        del request.session['login_from']
    except:
        pass
    del_reset()
    if request.session.get('is_login', None) != True:
        request.session['login_from'] = http + "://" + host + "/chaxun/"
        return redirect('login')
    return render(request, 'chaxun/index.html')

@csrf_exempt
def all(request):
    try:
        del request.session['login_from']
    except:
        pass
    del_reset()
    if request.is_secure():
        http = "https"
    else:
        http = "http"
    host = request.META['HTTP_HOST']
    request.session['login_from'] = http + "://" + host + "/"
    if request.session.get('is_login', None) != True:
        return redirect('login')
    user_email = request.session.get('user_email', None)
    if request.method == 'GET':
        search_order_id = request.GET.get('search_order_id', None)
        search_order_type = request.GET.get('search_order_type', None)
        search_order_status = request.GET.get('search_order_status', None)
        # search_kw = request.GET.get('search_kw', None)
        page = request.GET.get('page')
        num = request.GET.get('rows')
        if page and num and page != "NaN":
            right_boundary = int(page) * int(num)

        # 如果搜索关键字不为空，则根据此关键字模糊查询订单号和支付方式
        if search_order_id != "":
            if page and num and page != "NaN":
                page_user = Order.objects.filter(order_id=search_order_id, user_email=user_email).order_by('-order_id')[int(num) * (int(page) - 1):right_boundary]
            else:
                page_user = Order.objects.filter(order_id=search_order_id, user_email=user_email).order_by('-order_id')
            # 获取查询结果的总条数
            total = Order.objects.filter(order_id=search_order_id, user_email=user_email).count()
        elif search_order_type != "all" and search_order_status == "all":
            if page and num and page != "NaN":
                page_user = Order.objects.filter(order_type=search_order_type, user_email=user_email).order_by('-order_id')[int(num) * (int(page) - 1):right_boundary]
            else:
                page_user = Order.objects.filter(order_type=search_order_type, user_email=user_email).order_by('-order_id')
            # 获取查询结果的总条数
            total = Order.objects.filter(order_type=search_order_type, user_email=user_email).count()
        elif search_order_status != "all" and search_order_type == "all":
            if page and num and page != "NaN":
                page_user = Order.objects.filter(order_status=search_order_status, user_email=user_email).order_by('-order_id')[int(num) * (int(page) - 1):right_boundary]
            else:
                page_user = Order.objects.filter(order_status=search_order_status, user_email=user_email).order_by('-order_id')
            # 获取查询结果的总条数
            total = Order.objects.filter(order_status=search_order_status, user_email=user_email).count()
        elif search_order_type != "all" and search_order_status != "all":
            if page and num and page != "NaN":
                page_user = Order.objects.filter(order_status=search_order_status, order_type=search_order_type, user_email=user_email).order_by('-order_id')[int(num) * (int(page) - 1):right_boundary]
            else:
                page_user = Order.objects.filter(order_status=search_order_status, order_type=search_order_type, user_email=user_email).order_by('-order_id')
            # 获取查询结果的总条数
            total = Order.objects.filter(order_status=search_order_status, order_type=search_order_type, user_email=user_email).count()
        else:
            # 根据前台传来的分页信息，页码（page）和每页条数（rows）,计算分页后的user对象片段，例如前台传来第2页的参数，
            # rows=10，page=2，则服务端需要给前台返回[10:20]的数据片段，切片是左闭右开，所以最大只会取到下标为10到19，共10个数据
            if page and num and page != "NaN":
                page_user = Order.objects.filter(user_email=user_email).order_by('-order_id')[int(num) * (int(page) - 1):right_boundary]
                total = Order.objects.filter(user_email=user_email).count()
            else:
                page_user = Order.objects.filter(user_email=user_email).order_by('-order_id')[0:]
                # server端分页时必须返回total和rows,total用于分页时显示总数
                total = Order.objects.filter(user_email=user_email).count()
        # rows为具体数据
        rows = []
        # 遍历查询出的user对象，将对应数据放到rows中
        for user in page_user:
            if user.order_status == "已支付":
                rows.append({'order_id': user.order_id, 'order_name': user.order_name, 'qr_price': user.qr_price, 'order_type': user.order_type, 'add_date': user.add_date, 'last_save': user.last_save, 'user_ip': user.user_ip, 'order_status': user.order_status, 'kami': user.kami})
            else:
                rows.append({'order_id': user.order_id, 'order_name': user.order_name, 'qr_price': user.qr_price, 'order_type': user.order_type, 'add_date': user.add_date, 'last_save': user.last_save, 'user_ip': user.user_ip, 'order_status': user.order_status, 'kami': ""})
        # return render(request, 'account/user_management.html', {'rows': json.dumps(rows, cls=DateEncoder)})
        # rows = json.dumps(rows, cls=DecimalEncoder)
        #return render(request, 'chaxun/index.html', json.dumps({'total': total, 'rows': rows}, cls=DateEncoder))
        #return render(request, 'chaxun/index.html', {'total': total, 'rows': json.dumps(rows, cls=DateEncoder)})
        # 序列化数据，因为有datetime类型数据，所以使用自定义类DateEncoder序列化
        return HttpResponse(json.dumps({'total': total, 'rows': rows}, cls=DateEncoder))


@csrf_exempt
def chaxun_quxiao(request):
    if request.method != "POST":
        return HttpResponse("请求方式错误！")
    order_id = request.POST.get('quxiao_id', '')
    try:
        Order.objects.filter(order_id=order_id).update(order_status="已取消",  last_save=timezone.now())
        for i in Order.objects.filter(order_id=order_id).values('kami'):
            kami = i["kami"]
            Kami.objects.filter(kami=kami).update(use=0, last_save=timezone.now())
    except:
        msg = order_id + "数据库错误！"
        return HttpResponse(order_id)
    return HttpResponse("订单取消成功！")


def login(request):
    del_reset()
    if request.is_secure():
        http = "https"
    else:
        http = "http"
    host = request.META['HTTP_HOST']
    if request.method == 'GET':
        #记住来源的url，如果没有则设置为首页('/')
        if request.session['login_from'] == http + "://" + host + "/chaxun/":
            pass
        else:
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
            if request.session['login_from'] == http + "://" + host + "/chaxun/login/":
                request.session['login_from'] = http + "://" + host + "/chaxun/"
            elif request.session['login_from'] == http + "://" + host + "/chaxun/register/":
                request.session['login_from'] = http + "://" + host + "/"
    if request.session.get('is_login', None):
        if request.session['login_from'] == http + "://" + host + "/chaxun/login/":
            request.session['login_from'] = http + "://" + host + "/chaxun/"
        elif request.session['login_from'] == http + "://" + host + "/chaxun/register/":
            request.session['login_from'] = http + "://" + host + "/"
        return redirect(request.session['login_from'])
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的验证码！"
        if login_form.is_valid():  # 确保用户名和密码都不为空
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            password = hash_code(password)
            try:
                user = User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_email'] = user.email
                    request.session['user_cheak'] = user.password
                    request.session.set_expiry(0)
                    if request.session.get('is_login', None):
                        return redirect(request.session['login_from'])
                    return redirect('index')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'chaxun/login.html', locals())
    
    login_form = UserForm()
    return render(request, 'chaxun/login.html', locals())


def register(request):
    del_reset()
    if request.method == 'GET':
        #记住来源的url，如果没有则设置为首页('/')
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect(request.session['login_from'])
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的验证码！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'chaxun/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'chaxun/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'chaxun/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('login')  # 自动跳转到登录页面
        return render(request, 'chaxun/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'chaxun/register.html', locals())

def forgot(request):
    checkcodeGuoqi("","")
    if request.method == 'GET':
        #记住来源的url，如果没有则设置为首页('/')
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect(request.session['login_from'])
    if request.method == "POST":
        if request.session.get('email_checked', None) == False:
            forgot_form = EmailCheckForm(request.POST)
            message = "验证码错误！"
            if forgot_form.is_valid():  # 确保邮箱不为空
                email = forgot_form.cleaned_data['email']
                try:
                    user = User.objects.get(email=email)
                except:
                    message = "用户不存在！"
                    return render(request, 'chaxun/forgot.html', locals())
                request.session['email_checked'] = True
                request.session['checked_email'] = user.email
                request.session['forgot_user'] = user.name
                sendCode(email)
                guoqi_time = timezone.now() + datetime.timedelta(minutes=1)
                request.session['guoqi_time'] = json.dumps(guoqi_time, cls=MyJSONEncoder)
                request.session['left_time'] = 60
                forgot_form = PasswdResetForm()
                message = False
                return render(request, 'chaxun/forgot.html', locals())
            else:
                return render(request, 'chaxun/forgot.html', locals())
        else:
            resent = request.POST.get('resent', '')
            if resent == "resent":
                sendCode(request.session['checked_email'])
                guoqi_time = timezone.now() + datetime.timedelta(minutes=1)
                request.session['guoqi_time'] = json.dumps(guoqi_time, cls=MyJSONEncoder)
                request.session['left_time'] = 60
            guoqi_time = json.loads(request.session['guoqi_time'], object_hook=object_hook)
            left_time = (guoqi_time - timezone.now()).seconds
            if left_time <= 0 or left_time > 60:
                left_time = 0
            request.session['left_time'] = left_time
            forgot_form = PasswdResetForm(request.POST)
            message = "验证码错误！"
            if forgot_form.is_valid():  # 确保密码都不为空
                checkcode = forgot_form.cleaned_data['checkcode']
                password1 = forgot_form.cleaned_data['password1']
                password2 = forgot_form.cleaned_data['password2']
                password = hash_code(password1)
                if password1 != password2:  # 判断两次密码是否相同
                    message = "两次输入的密码不同！"
                    return render(request, 'chaxun/forgot.html', locals())
                try:
                    user = User.objects.get(email=request.session['checked_email'])
                except:
                    message = "用户不存在！"
                    return render(request, 'chaxun/forgot.html', locals())
                checkcodeGuoqi("","")
                checkcodeinfo = EmailCheckCode.objects.filter(email=request.session['checked_email'], checkcode=checkcode).values("statu")
                if checkcodeinfo.exists():
                    statu0count = 0
                    statu2count = 0
                    for i in checkcodeinfo:
                        if i["statu"] == 0:
                            statu0count += 1
                        if i["statu"] == 2:
                            statu2count += 1
                    if statu0count == 0:
                        if statu2count > 0:
                            message = "邮箱验证码已过期！"
                            return render(request, 'chaxun/forgot.html', locals())
                        message = "邮箱验证码错误！"
                        return render(request, 'chaxun/forgot.html', locals())
                    elif statu0count > 1:
                        message = "数据表错误，请联系管理员！"
                        return render(request, 'chaxun/forgot.html', locals())
                else:
                    message = "邮箱验证码错误！"
                    return render(request, 'chaxun/forgot.html', locals())
                if user.password != password:
                    user.password = password
                    user.save()
                    request.session['passwd_changed'] = True
                    del request.session['email_checked']
                    del request.session['checked_email']
                    del request.session['forgot_user']
                    message = False
                    return render(request, 'chaxun/forgot.html', locals())
                    
                else:
                    message = "Ops！该死的忘记密码定律，你似乎想起你的密码了，继不继续随你！"
                    return render(request, 'chaxun/forgot.html', locals())
            else:
                
                return render(request, 'chaxun/forgot.html', locals())
        #return render(request, 'chaxun/forgot.html', locals())
    
    request.session['email_checked'] = False
    request.session['passwd_changed'] = False
    request.session['left_time'] = 0
    forgot_form = EmailCheckForm()
    return render(request, 'chaxun/forgot.html', locals())
    

def logout(request):
    host = request.META['HTTP_HOST']
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect(request.session['login_from'])
    request.session.flush()
    # flush会一次性清空session中所有内容，可以使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    return redirect(request.session['login_from'])


import hashlib
from django.http import HttpResponse
def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

import random,string
def sendCode(email):
    from_email = settings.DEFAULT_FROM_EMAIL
    emailcode=""
    num=string.ascii_letters+string.digits
    while True:
        for i in range(18):
            emailcode+=random.choice(num)
        if checkcodeGuoqi(email,emailcode):
            break
    EmailCheckCode.objects.create(email=email, checkcode=emailcode, statu=0, add_date=timezone.now(), guoqi_data=timezone.now() + datetime.timedelta(minutes=15))
    subject = '重置密码'
    text_content = '您正在重置您在小龙卡密商城的账户密码！\n如果不是您本人操作请忽略此邮件即可!\n您的验证码是：' + emailcode
    html_content = '<p><strong style="color: red; font-size: 5">您正在重置您在小龙卡密商城的账户密码！<br>如果不是您本人操作请忽略此邮件即可!</strong></p><p>您的验证码是：<strong style="color: pink; font-size: 5">' + emailcode + '</strong></p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def checkcodeGuoqi(email,emailcode):
    emailcodeCheck = True
    for i in EmailCheckCode.objects.filter(statu=0).values('email','checkcode'):
        Cemail = i["email"]
        checkcode = i["checkcode"]
        for n in EmailCheckCode.objects.filter(email=Cemail, checkcode=checkcode, statu=0).values("id"):
            q = EmailCheckCode.objects.get(id=n["id"])
            if Cemail == email or q.was_guoqi() is True:
                q.statu=2
                q.save()
            elif q.was_guoqi() is False and emailcode == checkcode:
                emailcodeCheck = False
    return emailcodeCheck

def del_reset():
    try:
        del request.session['email_checked']
        del request.session['checked_email']
        del request.session['forgot_user']
        del request.session['passwd_changed']
        del request.session['left_time']
        del request.session['guoqi_time']
    except:
        pass
