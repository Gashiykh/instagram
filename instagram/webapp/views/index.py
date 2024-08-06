from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef, Subquery
from django.views.generic import ListView

from webapp.models import Follow, Like, Post


class IndexListView(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    model = Post
    template_name = 'instagram/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        following = Follow.objects.filter(follower=self.request.user)
        users = get_user_model().objects.filter(followers__in=following)
        context['posts'] = (
            Post.objects.filter(author__in=users)
            .annotate(liked=Exists(Subquery(Like.objects.filter(
                post=OuterRef('id'),
                author=self.request.user
            ))))
            .order_by('-created_at')
        )

        users = get_user_model().objects.exclude(followers__in=following)
        context['recommended_posts'] = Post.objects.filter(author__in=users)

        return context
