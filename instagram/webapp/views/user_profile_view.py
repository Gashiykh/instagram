from django.views.generic import DetailView

from accounts.models import User
from webapp.models import Follow


class UserProfileView(DetailView):
    model = User
    pk_url_kwarg = 'user_id'
    template_name = 'instagram/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            Follow.objects.get(follower=self.request.user, following=self.object)
        except Follow.DoesNotExist:
            context['follows'] = False
        else:
            context['follows'] = True

        return context
