from django import forms
from apps.core.forms import FormMixin


class EditNewsCategoryForm(forms.Form, FormMixin):

    pk = forms.IntegerField(error_messages={"required": "必须传入分类的id"})
    name = forms.CharField(max_length=100)
