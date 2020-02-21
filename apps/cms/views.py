from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


def login_view(request):
    return render(request, 'cms/login.html')


@staff_member_required(login_url='news:index')
def index(request):
    return render(request, 'cms/index.html')
