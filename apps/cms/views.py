from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from apps.cms.forms import EditNewsCategoryForm
from apps.core import Response
from apps.news.models import NewCategory


def login_view(request):
    return render(request, 'cms/login.html')


@staff_member_required(login_url='news:index')
def index(request):
    return render(request, 'cms/index.html')


class WriteNews(View):

    def get(self, request):
        return render(request, 'cms/write_news.html')


@require_GET
def news_category(request):
    categories = NewCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'cms/news_category.html', context=context)


@require_POST
def add_news_category(request):
    name = request.POST.get('name')
    exists = NewCategory.objects.filter(name=name).exists()
    if not exists:
        NewCategory.objects.create(name=name)
        return Response.response()
    else:
        return Response.params_error(message="该分类已经存在")


@require_POST
def edit_news_category(request):
    form = EditNewsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewCategory.objects.filter(pk=pk).update(name=name)
            return Response.response()
        except:
            return Response.params_error(message="该分类已经存在")
    else:
        return Response.params_error(message=form.get_errors())


@require_POST
def delete_news_category(request):
    pk = request.POST.get('pk')
    try:
        NewCategory.objects.filter(pk=pk).delete()
        return Response.response()
    except NewCategory.DoesNotExist:
        return Response.params_error(message="该分类已经存在")
