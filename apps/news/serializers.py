from rest_framework import serializers
from . models import News, NewCategory
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
