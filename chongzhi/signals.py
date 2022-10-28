from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from .chuli import guoqi
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from .models import Order

def payment_notification(sender, **kwargs):
    ipn_obj = sender
    aaa = open("/var/www/index/a.html", "a", encoding="utf-8")
    a_w = '<p>一次sender:</br>'
    a_w += str(type(ipn_obj)) + "|"
    a_w += str(ipn_obj.payment_status) + str(type(ipn_obj.payment_status)) + "</br>"
    a_w += str(ipn_obj.receiver_email) + "</br>"
    a_w += str(ipn_obj.invoice) + "</br>"
    a_w += str(ipn_obj.mc_gross) + "</br>"
    a_w += str(ST_PP_COMPLETED) + "</br>"
    a_w += "</p>"
    aaa.write(a_w)
    aaa.close()
    if ipn_obj.payment_status == "Completed":
        
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email == "longhuan_en@qq.com":
           
            # Not a valid payment
            order_id = ipn_obj.invoice
            qr_price = ipn_obj.mc_gross
            order_type = "paypal"
            # ALSO: for the same reason, you need to check the amount
            # received, `custom` etc. are all what you expect or what
            # is allowed.

            # Undertake some action depending upon `ipn_obj`.
            guoqi()
            try:
                chaxun = Order.objects.filter(order_id=order_id, qr_price=qr_price, order_type=order_type).values("order_status","kami","user_email")
            except:
                return "查询数据库错误！"
            if chaxun:
                for i in chaxun:
                    order_status = i["order_status"]
                    kami = i["kami"]
                    user_email = i["user_email"]
                    if order_status == "已取消":
                        beizhu = "疑似取消订单后支付"
                        Order.objects.filter(order_id=order_id).update(beizhu=beizhu, last_save=timezone.now())
                    if order_status == "未支付" or order_status == "已过期":
                        Order.objects.filter(order_id=order_id).update(order_status="已支付", last_save=timezone.now())
                        Kami.objects.filter(kami=kami).update(use=2, last_save=timezone.now())
                        from_email = settings.DEFAULT_FROM_EMAIL
                        subject = '订单' + str(order_id) + '支付成功'
                        text_content = '您的卡密是：' + kami
                        html_content = '<p>您的卡密是：<strong style="color: pink; font-size: 5">' + kami + '</strong></p>'
                        msg = EmailMultiAlternatives(subject, text_content, from_email, [user_email])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
    else:
        return "订单错误！"

valid_ipn_received.connect(payment_notification)