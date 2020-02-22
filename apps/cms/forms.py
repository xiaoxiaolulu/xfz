from django import forms
from apps.core.forms import FormMixin
from apps.news.models import News


class EditNewsCategoryForm(forms.Form, FormMixin):

    pk = forms.IntegerField(error_messages={"required": "必须传入分类的id"})
    name = forms.CharField(max_length=100)


class WriteNewsForm(forms.ModelForm, FormMixin):

    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']
