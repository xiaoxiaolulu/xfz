from django import forms
from django.core.cache import cache
from apps.core.forms import FormMixin
from apps.xfzauth.models import User


class LoginForm(forms.Form, FormMixin):

    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=20, min_length=6)
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):

    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20, min_length=6, error_messages={"max_length": "密码最多不能超过20个字符！", "min_length": "密码最少不能少于6个字符！"})
    password2 = forms.CharField(max_length=20, min_length=6, error_messages={'max_length': "密码最多不能超过20个字符", "min_length": "密码最少不能少于6个字符"})
    img_captcha = forms.CharField(max_length=4, min_length=4)
    sms_captcha = forms.CharField(max_length=4, min_length=4)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致')

        img_captcha = cleaned_data.get('img_captcha')
        cached_img_captcha = cache.get(img_captcha.lower())
        if not cached_img_captcha or cached_img_captcha.lower() != img_captcha.lower():
            raise forms.ValidationError("图像验证码错误！")

        telephone = cleaned_data.get("telephone")
        sms_captcha = cleaned_data.get('sms_captcha')
        cached_sms_captcha = cleaned_data.get(telephone)

        if not cached_sms_captcha or cached_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('短信验证码错误！')

        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            forms.ValidationError('该手机号码已经被注册！')
