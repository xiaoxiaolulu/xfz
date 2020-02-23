from django.http import Http404
from django.shortcuts import render
from apps.core import Response
from apps.news.forms import PublicCommentForm
from apps.news.models import News, NewCategory, Comment
from django.conf import settings

from apps.news.serializers import NewsSerializers, CommentSerializer


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    news = News.objects.select_related('category', 'author').all()[0: count]
    categories = NewCategory.objects.all()
    context = {
        'news': news,
        'categories': categories
    }
    return render(request, 'news/index.html', context=context)


def new_list(request):
    page = int(request.GET.get('p', 1))
    category_id = int(request.GET.get('category_id', 0))

    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:
        news = News.objects.select_related('category', 'author').all()[start: end]
    else:
        news = News.objects.select_related('category', 'author').filter(category__id=category_id)[start: end]
    serializer = NewsSerializers(news, many=True)
    data = serializer.data
    return Response.response(data=data)


def news_detail(request, news_id):
    try:
        news = News.objects.select_related('category', 'author').prefetch_related('comments__author').get(pk=news_id)
    except News.DoesNotExist:
        raise Http404
    context = {
        'news': news
    }
    return render(request, 'news/news_detail.html', context=context)


def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content, news=news, author=request.user)
        serializer = CommentSerializer(comment)
        return Response.response(data=serializer.data)
    else:
        return Response.params_error(message=form.get_errors())


def search(request):
    return render(request, 'search/search.html')
