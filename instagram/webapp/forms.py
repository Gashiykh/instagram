from django import forms

from webapp.models import Post, Image, Comment



class UserSearchForm(forms.Form):
    search_string = forms.CharField(max_length=100, required=False)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description']

    def clean_post(self):
        cleaned_data = super().clean()
        description = self.files.getlist('description')
        if not description:
            raise forms.ValidationError('Придумайте описание')
        return cleaned_data
    

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={"allow_multiple_selected": True})
        }

    def clean(self):
        cleaned_data = super().clean()
        images = self.files.getlist('image')
        if not images:
            raise forms.ValidationError('Необходимо загрузить хотя бы одно изображение')
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
