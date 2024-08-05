from django import forms
from django.forms import modelformset_factory

from webapp.models import Post, Image


class UserSearchForm(forms.Form):
    search_string = forms.CharField(max_length=100, required=False)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description']


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ImageForm(forms.Form):
    images = MultipleFileField(label='Выберите картинки', required=False)


