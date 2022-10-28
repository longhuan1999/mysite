from django.urls import path
from django.views.static import serve
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('', views.index, name='index'),
    path('tijiao', views.tijiao, name='tijiao'),
    path('queren', views.queren, name='queren'),
    path('jiegou', views.jiegou, name='jiegou'),
    path('test', views.test, name='test'),
    path('shoukuan', views.shoukuan),
    path('quxiao', views.quxiao, name='quxiao'),
    path('redirect_url', views.redirect_url),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin', views.add_kami, name="admin"),
    path('order_info', views.order_info, name="order_info"),
    path('logout', views.logout),
    path('paypal', include('paypal.standard.ipn.urls')),
]