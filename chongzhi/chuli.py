from .models import Kami, Order
from django.utils import timezone
import requests
import os, os.path
from django.db.models import Q
""" import re
import json
import urllib.request """
import decimal
import json,urllib.request
from urllib.parse import urlencode

def USD():
    url = 'http://api.k780.com'
    params = {
        'app' : 'finance.rate',
        'scur' : 'USD',
        'tcur' : 'CNY',
        'appkey' : 'XXXXX',
        'sign' : 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        'format' : 'json',
    }
    params = urlencode(params)

    f = urllib.request.urlopen('%s?%s' % (url, params))
    nowapi_call = f.read()
    #print content
    a_result = json.loads(nowapi_call)
    if a_result:
        if a_result['success'] != '0':
            return a_result['result']
        else:
            return a_result['result']
    else:
       return 'Request nowapi fail.'

""" def USD():
    url = "http://webforex.hermes.hexun.com/forex/quotelist?code=FOREXUSDCNY&column=Code,Price"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = urllib.request.Request(url=url, headers=headers)
    f = urllib.request.urlopen(req)
    html = f.read().decode("utf-8")
    s = re.findall("{.*}",str(html))[0]
    sjson = json.loads(s)
    USDCNY = sjson["Data"][0][0][1]/10000
    USDCNY = decimal.Decimal(USDCNY)
    return USDCNY """


def guoqi():
    for i in Order.objects.filter(order_status='未支付').values('kami', 'order_id', 'order_type'):
        kami = i["kami"]
        order_id = i["order_id"]
        order_type = i["order_type"]
        q = Order.objects.get(order_id=order_id, order_status='未支付')
        if order_type != "paypal":
            if q.was_guoqi() is True:
                q1 = Order.objects.filter(kami=kami, order_status='已支付')
                q2 = Kami.objects.filter(kami=kami).values('use')
                use = q2[0]["use"]
                if q1.exists() == False:
                    Order.objects.filter(order_id=order_id).update(order_status='已过期', last_save=timezone.now())
                    Kami.objects.filter(kami=kami).update(use=0, last_save=timezone.now())
                else:
                    Order.objects.filter(order_id=order_id).update(order_status='已过期', last_save=timezone.now())
                    if use != 2:
                        Kami.objects.filter(kami=kami).update(use=2, last_save=timezone.now())
                q_path = "/var/www/mysite/static/images/" + str(order_id) + ".png"
                if os.path.exists(q_path):
                    os.remove(q_path)
    
    for i in Order.objects.filter(order_status='已过期').values('order_id'):
        order_id = i["order_id"]
        q_path = "/var/www/mysite/static/images/" + str(order_id) + ".png"
        if os.path.exists(q_path):
            os.remove(q_path)

    for i in Order.objects.filter(order_status='已取消').values('order_id', 'kami'):
        order_id = i["order_id"]
        kami = i["kami"]
        q3 = Kami.objects.filter(kami=kami).values('use')
        q4 = Order.objects.filter(kami=kami, order_status='已支付')
        use = q3[0]["use"]
        if q4.exists() == False:
            if use == 1:
                Kami.objects.filter(kami=kami).update(use=0, last_save=timezone.now())
        elif q4.exists() == True and use != 2:
            Kami.objects.filter(kami=kami).update(use=2, last_save=timezone.now())
        q_path = "/var/www/mysite/static/images/" + str(order_id) + ".png"
        if os.path.exists(q_path):
            os.remove(q_path)
    

def order_count(user_email, csrftoken):
    order_ci = 0
    a = Order.objects.filter(Q(order_status='未支付', user_email=user_email) | Q(order_status='未支付', csrftoken=csrftoken))
    if a != None:

        for i in a:
            order_ci += 1
        if order_ci >= 3:
            return False
        else:
            return True
    else:
        return True


def sign_md5(order_id, order_price):
    import hashlib
    #order_price = str(order_price)
    sign1 = order_id + order_price
    sign1 = sign1.encode(encoding='utf-8')
    m = hashlib.md5()
    m.update(sign1)
    sign1_md5 = m.hexdigest()
    sign = sign1_md5 + 'Long19990224'
    sign = sign.encode(encoding='utf-8')
    n = hashlib.md5()
    n.update(sign)
    sign = n.hexdigest()
    return sign

def sign2_md5(type, price): #type, price
    import hashlib
    sign1 = price + type
    sign1 = sign1.encode(encoding='utf-8')
    m = hashlib.md5()
    m.update(sign1)
    sign1_md5 = m.hexdigest()
    sign = sign1_md5 + 'Long19990224'
    sign = sign.encode(encoding='utf-8')
    n = hashlib.md5()
    n.update(sign)
    sign = n.hexdigest()
    return sign


def post_order(order_id, order_type, order_price, order_name, sign, extension):
    post_data = {
        "order_id": order_id,
        "order_type": order_type,
        "order_price": order_price,
        "order_name": order_name,
        "sign": sign,
        "redirect_url": "https://buy.warryme.com/chongzhi/redirect_url",
        "extension": extension
    }
    try:
        r = requests.post('http://207.148.97.10:7001/api/order', json=post_data,
                          headers={'Content-Type': 'application/json;charset=UTF-8'})
    except:
        r = {'msg': '支付系统异常！'}
    return r
    '''print(r.status_code)
    print(r.url)
    print(r.json())'''

def GET_order(sign, type, price):
    GET_data = {
        "sign": sign,
        "type": type,
        "price": price
    }

    r = requests.get('http://207.148.97.10:7001/addons/pay/api/notify', params=GET_data)



def order_get(msg1):
    import urllib
    import requests
    from bs4 import BeautifulSoup
    order_id = msg1["order_id"]
    # import decimal # decimal.Decimal("%.2f" % float(x))
    Order.objects.filter(order_id=int(order_id)).update(qr_url=msg1["qr_url"], qr_price=msg1["qr_price"], last_save=timezone.now())
    for i in Order.objects.filter(order_id=msg1["order_id"]).values("add_date" ):
        created_at = i["add_date"]
    q = Order.objects.get(order_id=msg1["order_id"])
    guoqi_time = q.guoqi_time()
    pay_status = msg1["pay_status"]
    order_name = msg1["order_name"]
    qr_price = msg1["qr_price"]
    qr_url = msg1["qr_url"]
    left_time = (guoqi_time - created_at).seconds
    if msg1["order_type"] == "alipay":
        order_type = "支付宝"
        qr_url = qr_url + r"%26m%3d" + order_id
        qr_url = urllib.parse.quote(qr_url)
        type = "tEaTWFrqy8shMHYvLtZSMao"
        #img_url = "http://qr.liantu.com/api.php?text=" + qr1_url
    elif msg1["order_type"] == "wechat":
        order_type = "微信"
        type = "sEuSBQq6msIhMHcmKdRcP6I"
    qp_url = "https://cli.im/api/qrcode/code?text=" + qr_url + "&mhid=" + type
    res = requests.get(qp_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    list1 = soup.select('img')
    list1 = str(list1)[6:-3]
    list1 = list1.split()
    list1 = list1[2][7:-1]
    list2 = list1.split("/")
    da = list2[2].find("data")
    img_url = "https://" + list2[0] + "/" + list2[1] + "/down?" +list2[2][da:] + "&type=png"
    img_url = img_url.replace("amp;", "")

    res = requests.get(img_url)
    #order_id = str(order_id)
    with open('/var/www/mysite/static/images/{}.png'.format(order_id), 'wb+') as f:  # /var/www/mysite/static/images/1.png
        f.write(res.content)
        f.close()

        img_url = "/static/images/" + order_id + ".png"
    msg = {"left_time": left_time, "kami": "", "created_at": created_at, "guoqi_time": guoqi_time, "pay_status": pay_status, "order_id": order_id, "order_type": order_type, "order_name": order_name, "qr_url": qr_url, "qr_price": qr_price, "img_url": img_url}
    return msg


""" def del_guoqi():
    for i in Order.objects.filter(order_status='已过期').values('order_id'):
        order_id = i["order_id"]
        q_path = "/var/www/mysite/static/images/" + str(order_id) + ".png"
        if os.path.exists(q_path):
            os.remove(q_path)


def del_cancel():
    for i in Order.objects.filter(order_status='已取消').values('order_id', 'kami'):
        order_id = i["order_id"]
        kami = i["kami"]
        Kami.objects.filter(kami=kami).update(use=0, last_save=timezone.now())
        q_path = "/var/www/mysite/static/images/" + str(order_id) + ".png"
        if os.path.exists(q_path):
            os.remove(q_path) """