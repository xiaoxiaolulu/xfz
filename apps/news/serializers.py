from rest_framework import serializers
from .models import News, NewCategory, Comment, Banner
from ..xfzauth.serializers import UserSerializer


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewCategory
        fields = ('id', 'name')


class NewsSerializers(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    author = UserSerializer()

    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'thumbnail', 'pub_time', 'category', 'author')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'pub_time')


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ('id', 'image_url', 'priority', 'link_to')
