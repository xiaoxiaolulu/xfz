from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST

from apps.core import Response
from apps.xfzauth.forms import LoginForm


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
