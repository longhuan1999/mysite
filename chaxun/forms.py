from django import forms
from . import models
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    captcha = CaptchaField(label='验证码')
    '''
    class Meta:
        model = models.User
        fields = ['name', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, *kwargs)
        self.fields['name'].label = '用户名'
        self.fields['password'].label = '密码'
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})'''

class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))
    email = forms.EmailField(label="邮箱", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入下单时的邮箱，否则无法查询订单'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')

class EmailCheckForm(forms.Form):
    email = forms.EmailField(label="邮箱", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入您的邮箱'}))
    captcha = CaptchaField(label='验证码')

class PasswdResetForm(forms.Form):
    checkcode = forms.CharField(label="邮箱验证码", max_length=18, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱验证码'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))
    captcha = CaptchaField(label='验证码')