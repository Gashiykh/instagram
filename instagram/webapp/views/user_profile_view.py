from django.views.generic import DetailView

from accounts.models import User


class UserProfileView(DetailView):
    model = User
    pk_url_kwarg = 'user_id'
    template_name = 'instagram/user_profile.html'
