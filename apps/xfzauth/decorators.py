from functools import wraps
from django.http import Http404
from django.shortcuts import redirect
from apps.core import Response


def xfz_login_required(func):
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return Response.unauth(message="请先登录")
            else:
                return redirect('news:index')

    return wrapper


def xfz_superuser_required(func):

    @wraps(func)
    def decorator(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            raise Http404()
    return decorator
