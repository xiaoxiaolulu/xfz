import random
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from apps.core import Response
from apps.core.captcha.xfzcaptcha import Captcha
from apps.xfzauth.forms import LoginForm, RegisterForm
from io import BytesIO

from apps.xfzauth.models import User


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():

        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=telephone, password=password)

        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return Response.response()
            else:
                return Response.unauth(message="账号被冻结！")
        else:
            return Response.params_error(message='手机或者密码错误')
    else:
        errors = form.get_errors()
        return Response.params_error(message=errors)


def logout_view(request):
    logout(request)
    return redirect(reverse('news:index'))


def img_captcha(request):
    text, image = Captcha.gene_code()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()
    cache.set(text.lower(), text.lower(), 5 * 60)
    return response


def sms_captcha(request):
    telephone = request.GET.get('telephone')
    code = ''.join([str(random.randint(0, 9)) for i in range(0, 4)])
    cache.set(telephone, code, 5 * 60)
    print(f"{telephone} {code}")
    return Response.response()


@require_POST
def register(request):
    global user

    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        try:
            user = User.objects.create_user(telephone=telephone, username=username, password=password)
        except User.DoesNotExist:

            login(request, user)
        return Response.response()
    else:
        return Response.params_error(message=form.get_errors())
