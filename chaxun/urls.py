from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('chaxun_quxiao/', views.chaxun_quxiao, name='chaxun_quxiao'),
    path('forgot/', views.forgot, name='forgot'),
    path('captcha', include('captcha.urls')),
    path('all/', views.all)
]