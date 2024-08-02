from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = [
            'username', 'email', 'avatar',
            'password1', 'password2', 'first_name',
            'description', 'phone_number', 'gender',
            ]
