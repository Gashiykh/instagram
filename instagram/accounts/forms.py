from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from django import forms


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = [
            'username', 'email', 'avatar',
            'password1', 'password2', 'first_name',
            'description', 'phone_number', 'gender',
            ]


class LoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        if username_or_email and password:
            user = authenticate(request=self.request, username=username_or_email, password=password)
            if user is None:
                try:
                    user = authenticate(request=self.request, email=username_or_email, password=password)
                except Exception as e:
                    user = None
                if user is None:
                    raise forms.ValidationError('Неправильный логин или пароль')
            self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username', 'email', 'avatar',
            'first_name', 'description', 'phone_number', 'gender'
        ]
