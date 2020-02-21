from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from apps.core import Response
from apps.core.captcha.xfzcaptcha import Captcha
from apps.xfzauth.forms import LoginForm
from io import BytesIO


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
    return response
