import os

from django.http import FileResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from apps.core import Response
from apps.payinfo.models import PayInfo, PayInfoOrder
from apps.xfzauth.decorators import xfz_login_required
from xfz import settings


def payinfo(request):
    context = {
        'payinfos': PayInfo.objects.all()
    }
    return render(request, 'payinfo/payinfo.html', context=context)


@xfz_login_required
def payinfo_order(request):
    payinfo_id = request.GET.get('payinfo_id')
    payinfo = PayInfo.objects.get(pk=payinfo_id)
    order = PayInfoOrder.objects.create(payinfo=payinfo, buyer=request.user, status=1, amount=payinfo.price)
    context = {
        'goods': {
            'thumbnail': '',
            'title': payinfo.title,
            'price': payinfo.price
        },
        'order': order,
        # /course/notify_url/
        'notify_url': request.build_absolute_uri(reverse('payinfo:notify_view')),
        'return_url': request.build_absolute_uri(reverse('payinfo:index'))
    }
    return render(request, 'course/course_order.html', context=context)


@csrf_exempt
def notify_view(request):
    orderid = request.POST.get('orderid')
    PayInfoOrder.objects.filter(pk=orderid).update(status=2)
    return Response.response()


@xfz_login_required
def download(request):
    payinfo_id = request.GET.get('payinfo')
    order = PayInfoOrder.objects.filter(payinfo_id=payinfo_id, buyer=request.user,  status=2).first()

    if order:
        payinfo = order.payinfo
        fp = open(os.path.join(settings.MEDIA_ROOT, payinfo.path), 'rb')
        response = FileResponse(fp)
        response['Content-type'] = 'image/jpeg'
        response['Content-Disposition'] = 'attachment; filename="%s"' % payinfo.path('/')[-1]
        return response
    else:
        return Http404
