from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        if username is None or password is None:
            return None
        
        try:
            user = get_user_model().objects.get(email=username)

        except get_user_model().DoesNotExist:

            try:
                user = get_user_model().objects.get(username=username)

            except get_user_model().DoesNotExist:
                return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None