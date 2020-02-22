from django.shortcuts import render
from apps.news.models import News, NewCategory
from django.conf import settings


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    news = News.objects.order_by('-pub_time')[0: count]
    categories = NewCategory.objects.all()
    context = {
        'news': news,
        'categories': categories
    }
    return render(request, 'news/index.html', context=context)


def new_list(request):
    page = int(request.GET.get('p', 1))
    start = (page-1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT
    news = News.objects.order_by('-pub_time')[start: end]


def news_detail(request, news_id):
    print(news_id)
    return render(request, 'news/news_detail.html')


def search(request):
    return render(request, 'search/search.html')