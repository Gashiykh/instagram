from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.generic import ListView

from webapp.models import Post, Follow


class IndexListView(ListView):
    context_object_name = 'posts'
    model = Post
    template_name = 'instagram/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        following = Follow.objects.filter(follower=self.request.user)
        users = get_user_model().objects.filter(followers__in=following)
        context['posts'] = (Post.objects.filter(author__in=users)
                            .order_by('-created_at'))

        users = get_user_model().objects.exclude(followers__in=following)
        context['recommended_posts'] = Post.objects.filter(author__in=users)

        return context
