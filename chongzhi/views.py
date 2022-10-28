from django.shortcuts import render, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
import datetime
from django.utils import timezone
from django.http import HttpResponse
from .models import Kami, Taocan, Order, APP_POST, Shangpin
from .chuli import guoqi, order_count, sign_md5, sign2_md5, post_order, order_get, GET_order, USD
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from functools import wraps
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from urllib.parse import urlsplit
from requests import request
import decimal
#http = urlsplit(request.build_absolute_url(None)).scheme
#获得当前的HTTP或HTTPS



# Create your views here.
@csrf_exempt
def index(request):
    del_reset()
    if request.is_secure():
        http = "https"
    else:
        http = "http"
    try:
        del request.session['login_from']
    except:
        pass
    host = request.META['HTTP_HOST']
    request.session['login_from'] = http + "://" + host
    guoqi()
    msg = {}
    taocan_list = []
    shangpin_list = []
    for i in Shangpin.objects.values('shangpin'):
        shangpin = i['shangpin']
        shangpin_list.append(shangpin)
    msg['shangpin'] = shangpin_list
    if request.method == "POST":
        sp_selected = request.POST.get('shangpin', None)
        if sp_selected == "请选择商品":
            selected = ""
        else:
            selected = request.POST.get('taocan', None)
        for i in Taocan.objects.filter(shangpin=sp_selected).values('taocan'):
            taocan = i['taocan']
            taocan_list.append(taocan)
        msg['taocan'] = taocan_list
        kucun = 0
        alipay_price = ''
        wechat_price = ''
        if selected != "" and selected != "请选择套餐":
            if selected in taocan_list:
                for price in Taocan.objects.filter(taocan=selected).values('alipay_price', 'wechat_price'):
                    alipay_price = price['alipay_price']
                    wechat_price = price['wechat_price']
                    USDlist = USD()
                    if USDlist["rate"]:
                        paypal_price = alipay_price / decimal.Decimal(USDlist["rate"])
                        paypal_price = paypal_price.quantize(decimal.Decimal('0.00'), decimal.ROUND_UP)
                        msg['msgid'] = "汇率更新于：" + USDlist["update"]
                        if paypal_price < 2.06:
                            msg['msgid'] = "付款金额过低：" + str(paypal_price) + "\t汇率更新于：" + USDlist["update"]
                            paypal_price = "不支持"
                    elif USDlist["msgid"]:
                        paypal_price = "不支持"
                        msg['msgid'] = USDlist["msgid"] + ":" + USDlist["msg"]
                    elif USDlist == 'Request nowapi fail.':
                        paypal_price = "不支持"
                        msg['msgid'] = 'Request nowapi fail.'
                    
                for i in Kami.objects.filter(taocan=selected, use=0):
                    kucun += 1
                msg['taocan'] = taocan_list
                msg['alipay_price'] = alipay_price
                msg['wechat_price'] = wechat_price
                msg['paypal_price'] = paypal_price
                msg['kucun'] = kucun
                msg['select'] = selected
                msg['sp_select'] = sp_selected
                return render(request, 'chongzhi/index.html', {'msg': msg})

        msg['taocan'] = taocan_list
        msg['alipay_price'] = ''
        msg['wechat_price'] = ''
        msg['paypal_price'] = ''
        msg['kucun'] = ''
        msg['select'] = ''
        msg['sp_select'] = sp_selected
        return render(request, 'chongzhi/index.html', {'msg': msg})
    msg['alipay_price'] = ''
    msg['wechat_price'] = ''
    msg['paypal_price'] = ''
    msg['kucun'] = ''
    msg['select'] = ''
    msg['sp_select'] = ''
    # typeq = type(taocan)
    return render(request, 'chongzhi/index.html', {'msg': msg})


def tijiao(request):
    try:
        del request.session['login_from']
    except:
        pass
    guoqi()
    
    if request.method != "POST":
        return render(request, 'chongzhi/error.html')
    taocan = request.POST.get('slected_taocan', None)
    kucun = 0
    for i in Kami.objects.filter(taocan=taocan, use=0):
        kucun += 1
    if kucun == 0 or kucun == '':
        return render(request, 'chongzhi/sorry.html')
    zhifu = request.POST.get('zhifu','')
    if zhifu == 'paypal':
        zhifu_price = 'alipay_price'
        zhifu_name = 'PayPal'
    elif zhifu == 'alipay':
        zhifu_price = 'alipay_price'
        zhifu_name = '支付宝'
    elif zhifu == 'wechat':
        zhifu_price = 'wechat_price'
        zhifu_name = '微信'
    for price in Taocan.objects.filter(taocan=taocan).values(zhifu_price):
        price_queren = price[zhifu_price]
        request.session['price_queren'] = str(price_queren)
    msg = {}
    if zhifu == 'paypal':
        USDlist = USD()
        if USDlist["rate"]:
            price_queren = price_queren / decimal.Decimal(USDlist["rate"])
            price_queren = price_queren.quantize(decimal.Decimal('0.00'), decimal.ROUND_UP)
            request.session['price_queren'] = str(price_queren)
            msg['msgid'] = "汇率更新于：" + USDlist["update"]
            """ if price_queren < 2.06:
                msg['msgid'] = "付款金额过低：" + str(price_queren) + "\t汇率更新于：" + USDlist["update"]
                price_queren = "不支持" """
        elif USDlist["msgid"]:
            price_queren = "不支持"
            msg['msgid'] = USDlist["msgid"] + ":" + USDlist["msg"]
        elif USDlist == 'Request nowapi fail.':
            price_queren = "不支持"
            msg['msgid'] = 'Request nowapi fail.'
        """ price_queren = decimal.Decimal(price_queren / USDlist())
        price_queren = price_queren.quantize(decimal.Decimal('0.00'), decimal.ROUND_UP) """
        """ if price_queren < 2.06:
            price_queren = "不支持" """
    csrftoken = request.COOKIES.get('csrftoken')
    user_email = request.POST.get('user_email', '')
    if order_count(user_email, csrftoken) is False:
        return render(request, 'chongzhi/order_out.html')
    msg['taocan'] = taocan
    msg['zhifu'] = zhifu_name
    msg['price_queren'] = price_queren
    msg['user_email'] = user_email
    return render(request, 'chongzhi/queren.html', {'msg': msg})

@never_cache
@csrf_exempt
def queren(request):
    try:
        del request.session['login_from']
    except:
        pass
    guoqi()
    if request.method != "POST":
        return render(request, 'chongzhi/error.html')

    if request.POST.get('kami', None) != None:
        return render(request, 'chongzhi/error1.html')
    csrftoken = request.COOKIES.get('csrftoken')
    order_name = request.POST.get('taocan', '')
    kucun = 0
    for i in Kami.objects.filter(taocan=order_name,use=0):
        kucun += 1
    if kucun == 0 or kucun == '':
        return render(request, 'chongzhi/sorry.html')
    zhifu = request.POST.get('zhifu', None)
    if zhifu == 'PayPal':
        order_type = 'paypal'
    if zhifu == '支付宝':
        order_type = 'alipay'
    if zhifu == '微信':
        order_type = 'wechat'
    #order_price = decimal.Decimal(request.session['price_queren'])
    try:
        order_price = request.session['price_queren']
    except KeyError:
        return render(request, 'chongzhi/error.html')
    del request.session['price_queren']
    email = request.POST.get('email', None)
    if order_count(email, csrftoken) is False:
        return render(request, 'chongzhi/order_out.html')
    for i in Kami.objects.filter(taocan=order_name, use=0).values("kami"):
        kami = i["kami"]
    Kami.objects.filter(kami=kami).update(use=1, last_save=timezone.now())
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    Order.objects.create(kami=kami, order_name=order_name, order_status='未支付', add_date=timezone.now(), user_email=email, user_ip=ip, csrftoken=csrftoken,order_type=order_type)
    for i in Order.objects.filter(kami=kami).values('order_id'):
        order_id = i["order_id"]
    order_id = str(order_id)
    if zhifu == 'PayPal':
        # from .paypal_pay import view_that_asks_for_money
        # view_that_asks_for_money(request,order_price,order_name,order_id)
        Order.objects.filter(order_id=int(order_id)).update(qr_url="paypal", qr_price=order_price, last_save=timezone.now())
        paypal_dict = {
            "business": settings.PAYPAL_REVEIVER_EMAIL,
            "amount": order_price,
            "item_name": order_name,
            "invoice": order_id,
            'currency_code': 'USD',
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            # "notify_url": www.baidu.com/paypalview/,
            "return": request.build_absolute_uri(reverse('order_info')),
            # "notify_url": www.baidu.com/ret_paypal/,
            "cancel_return": request.build_absolute_uri(reverse('quxiao')),
            # "notify_url": www.baidu.com/can_paypal/,
            "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
        }
 
        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form}
        return render(request, "chongzhi/payment.html", context)
    else:
        sign = sign_md5(order_id, order_price)
        r = post_order(order_id, order_type, order_price, order_name, sign, extension=kami)
        try:
            msg1 = r.json()
        except:
            msg2 = r["msg"] + "   请联系管理员！QQ：2114467924"
            msg = {"msg": msg2}
            return render(request, 'chongzhi/sorry1.html', {"msg": msg})
        if "msg" in msg1:
            Kami.objects.filter(kami=kami).update(use=0, last_save=timezone.now())
            Order.objects.filter(order_id=int(order_id)).update(order_status="已取消", last_save=timezone.now(), beizhu="系统错误，自动取消")
            if msg1["msg"] == "系统火爆，请过1-3分钟后下单!":
                msg = {"msg": msg1["msg"]}
            else:
                msg2 = "未知错误："+msg1["msg"]+"   请联系管理员！QQ：2114467924"
                msg = {"msg": msg2}
            return render(request, 'chongzhi/sorry1.html', {"msg": msg})
        msg = order_get(msg1)
        return render(request, 'chongzhi/zhifu.html', {'msg': msg})

@csrf_exempt
def jiegou(request):
    try:
        del request.session['login_from']
    except:
        pass
    guoqi()
    
    if request.method != "POST":
        return render(request, 'chongzhi/error.html')
    order_id = request.POST.get('order_id', '')
    created_at = request.POST.get('created_at', '')
    img_url = request.POST.get('img_url', '')
    for i in Order.objects.filter(order_id=int(order_id)).values("kami", "order_status", "order_name", "qr_url", "qr_price", "order_type"):
        kami = i["kami"]
        
        order_status = i["order_status"]
        order_name = i["order_name"]
        qr_url = i["qr_url"]
        qr_price = i["qr_price"]
        order_type = i["order_type"]
    if order_type == "alipay":
        order_type = "支付宝"
    elif order_type == "wechat":
        order_type = "微信"
    q = Order.objects.get(order_id=int(order_id))
    guoqi_time = q.guoqi_time()
    left_time = (guoqi_time - timezone.now()).seconds
    if left_time <= 0 or left_time > 300:
        left_time = -1
    if order_status == "未支付":
        msg = {"left_time": left_time, "order_id": order_id, "kami": "", "guoqi_time": guoqi_time, "pay_status": order_status, "order_name": order_name, "qr_url": qr_url, "qr_price": qr_price, "order_type":order_type, "created_at": created_at, "img_url": img_url}
        
    elif order_status == "已支付":
        msg = {"left_time": -1, "order_id": order_id, "kami": kami, "guoqi_time": guoqi_time, "pay_status": order_status, "order_name": order_name, "qr_url": "/chongzhi", "qr_price": qr_price, "order_type":order_type, "created_at": created_at, "img_url": "https://www.warryme.com/qr_cover/zhifu.png"}
    
    elif order_status == "已过期":
        msg = {"left_time": left_time, "order_id": order_id, "kami": "", "guoqi_time": guoqi_time, "pay_status": order_status, "order_name": order_name, "qr_url": "/chongzhi", "qr_price": qr_price, "order_type":order_type, "created_at": created_at, "img_url": "https://www.warryme.com/qr_cover/shixiao.png"}
        

    return render(request, "chongzhi/zhifu.html", {"msg": msg})

@csrf_exempt
def quxiao(request):
    try:
        del request.session['login_from']
    except:
        pass
    referer_url = request.META.get("HTTP_REFERER")
    if request.method != "POST":
        if referer_url is None:
            guoqi()
            return render(request, 'chongzhi/error.html')
        elif "www.paypal.com" in referer_url:
            guoqi()
            return render(request, 'chongzhi/error-1.html')
        else:
            guoqi()
            return render(request, 'chongzhi/error.html')
    order_id = request.POST.get('quxiao_id', '')
    try:
        Order.objects.filter(order_id=order_id).update(order_status="已取消",  last_save=timezone.now())
    except:
        return render(request, 'chongzhi/error2.html')
    guoqi()
    return render(request, "chongzhi/quxiao.html")

def test(request):
    return render(request,"chongzhi/Untitled-1.html")

@csrf_exempt
def shoukuan(request):
    guoqi()
    aaa = open("/var/www/index/a.html", "a", encoding="utf-8")
    a_w = '<p>一次POST:</br>'
    aaa.write(a_w)
    aaa.close()
    if request.method != "POST":
        return render(request, 'chongzhi/error.html')

    json_data = request.body
    json_data = str(json_data, encoding="utf-8")
    json_dict = eval(json_data)
    qr_price = json_dict["money"]
    order_type = json_dict["type"]
    deviceid = json_dict["deviceid"]
    #aaa_text = qr_price + type(qr_price) + order_type + type(order_type) + deviceid + type(deviceid)
    aaa = open("/var/www/index/a.html", "a", encoding="utf-8")
    a_w = json_data + '</p>\n'
    aaa.write(a_w)
    aaa.close()
    if deviceid != "980224-ffffffff-c818-f87a-ffff-ffffef05ac4a":
        return HttpResponse("ERROR")
    else:
        APP_POST.objects.create(money=qr_price, encrypt=json_dict["encrypt"], time=json_dict["encrypt"], type=order_type, title=json_dict["title"], deviceid=deviceid, content=json_dict["content"])
        chaxun = Order.objects.filter(qr_price=qr_price, order_type=order_type).values("add_date","order_status","order_id","kami","user_email")
        guoqi_time1 = timezone.now() - datetime.timedelta(minutes=5)
        guoqi_time2 = timezone.now() - datetime.timedelta(minutes=6)
        if chaxun:
            for i in chaxun:
                add_date = i["add_date"]
                order_status = i["order_status"]
                order_id = i["order_id"]
                kami = i["kami"]
                user_email = i["user_email"]
                if add_date < guoqi_time1 and add_date >= guoqi_time2 and order_status == "已过期":
                    beizhu = "疑似超时支付"
                    Order.objects.filter(order_id=order_id).update(beizhu=beizhu, last_save=timezone.now())
                if add_date > guoqi_time1 and order_status == "已取消":
                    beizhu = "疑似取消订单后支付"
                    Order.objects.filter(order_id=order_id).update(beizhu=beizhu, last_save=timezone.now())
                if add_date >= guoqi_time1 and order_status == "未支付":
                    Order.objects.filter(order_id=order_id).update(order_status="已支付", last_save=timezone.now())
                    Kami.objects.filter(kami=kami).update(use=2, last_save=timezone.now())
                    from_email = settings.DEFAULT_FROM_EMAIL
                    subject = '订单' + str(order_id) + '支付成功'
                    text_content = '您的卡密是：' + kami
                    html_content = '<p>您的卡密是：<strong style="color: pink; font-size: 5">' + kami + '</strong></p>'
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [user_email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

        type = order_type
        price = qr_price
        sign = sign2_md5(type, price)
        GET_order(sign, type, price)
        return HttpResponse("SECCUSS")

@csrf_exempt
def redirect_url(request):
    return HttpResponse("OK!")


def check_login(f):
    @wraps(f)
    def inner(request, *arg, **kwargs):
        if request.session.get('is_login') == '1' and request.session.get('username') == 'admin':
            return f(request, *arg, **kwargs)
        else:
            return redirect('admin_login')
    return inner

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "longhuan" and password == "Long19990224!":
            # 登录成功
            # 1，生成特殊字符串
            # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
            # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
            request.session['is_login'] = '1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
            request.session['username']= 'admin'  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
            # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
            #request.session['user_id'] = user[0].id
            return redirect('admin')
        else:
            return render(request, 'chongzhi/admin_login.html')
        # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
    return render(request, 'chongzhi/admin_login.html')

def logout(request):
    del request.session['username']
    del request.session['is_login']
    #点退出删除保存的在数据库的ID  COOKie 不删还可以访问购物车
    return redirect('admin') #重定向到首页

@never_cache
@check_login
def add_kami(request):
    msg = {}
    taocan_list = []
    for i in Taocan.objects.values('taocan'):
        taocan = i['taocan']
        taocan_list.append(taocan)
    msg['taocan'] = taocan_list
    msg['return_list'] = ''
    if request.method == "POST":
        selected = request.POST.get('taocan', '')
        kamis = request.POST.get('kamis', '')
        kamis = kamis.replace(' ', '')
        kamis = kamis.replace('\r', '')
        kami_list = kamis.split('\n')
        return_list = ''
        if selected != "请选择套餐":
            for i in kami_list:
                if len(i) != 16 and len(i) != 18 and len(i) != 32 and len(i) != 36:
                    return_list += i + '，批量导入的卡密只能是16位或18位或32位或36位' + '\n'
                #elif i.isalnum() is False:
                    #return_list += i + '，批量导入的卡密只能是字母数字' + '\n'
                else:
                    try:
                        Kami.objects.create(kami=i, use=0, taocan_id=selected)
                        return_list += i + '，创建成功' + '\n'
                    except:
                        return_list += i + '，创建失败，此卡密可能已存在' + '\n'
        else:
            return_list = '错误：请选择套餐'
        return_list = return_list.replace("\r", '')
        msg["select"] = selected
        msg["return_list"] = return_list
        '''aaa_text = repr(return_list)
        aaa = open("/var/www/index/a.html", "w")
        aaa.write(aaa_text)
        aaa.close()'''
    return render(request, 'chongzhi/add_kami.html', {"msg": msg})

@csrf_exempt
def order_info(request):
    guoqi()
    referer_url = request.META.get("HTTP_REFERER")
    paymentid = request.GET.get("paymentId")
    if referer_url == None:
        return render(request, 'chongzhi/error.html')
    elif "www.paypal.com" in referer_url :
        msg = {}
        msg['paymentid'] = paymentid
        return render(request, 'chongzhi/paypal_success.html', {"msg": msg})
    else:
        return render(request, 'chongzhi/error.html')

def del_reset():
    try:
        del request.session['email_checked']
        del request.session['checked_email']
        del request.session['forgot_user']
        del request.session['passwd_changed']
    except:
        pass
