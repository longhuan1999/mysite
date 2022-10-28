from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
def view_that_asks_for_money(request,order_price,order_name,order_id):
    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_REVEIVER_EMAIL,
        "amount": order_price,
        "item_name": order_name,
        "invoice": order_id,
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