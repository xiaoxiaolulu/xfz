import os
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
import qiniu
from apps.cms.forms import EditNewsCategoryForm, WriteNewsForm, AddBannerForm, EditBannerForm
from apps.core import Response
from apps.news.models import NewCategory, News, Banner
from apps.news.serializers import BannerSerializer


def login_view(request):
    return render(request, 'cms/login.html')


@staff_member_required(login_url='news:index')
def index(request):
    return render(request, 'cms/index.html')


class WriteNews(View):

    def get(self, request):
        categories = NewCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'cms/write_news.html', context=context)

    def post(self, request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewCategory.objects.get(pk=category_id)
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail, content=content, category=category,
                                author=request.user)
            return Response.response()
        else:
            return Response.params_error(message=form.get_errors())


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


@require_POST
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return Response.response(data={'url': url})


@require_GET
def qntoken(request):
    ak = settings.QINIU_ACCESS_KEY
    sk = settings.QINIU_SECRET_KEY
    bucket = settings.QINIU_BUCKET_NAME
    q = qiniu.Auth(ak, sk)
    token = q.upload_token(bucket)
    return Response.response(data={'token': token})


def banners(request):
    return render(request, 'cms/banners.html')


def banner_list(request):
    banners = Banner.objects.all()
    serialize = BannerSerializer(banners, many=True)
    return Response.response(data=serialize.data)


def add_banner(request):
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority, image_url=image_url, link_to=link_to)
        return Response.response(data={'banner_id': banner.pk})
    else:
        return Response.response(message=form.get_errors())


def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    Banner.objects.filter(pk=banner_id).delete()
    return Response.response()


def edit_banner(request):

    form = EditBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        Banner.objects.filter(pk=pk).update(priority=priority, image_url=image_url, link_to=link_to)
        return Response.response()
    else:
        return Response.response(message=form.get_errors())