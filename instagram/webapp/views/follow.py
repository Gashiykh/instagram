from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from accounts.models import User
from webapp.models import Follow


class FollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        following = get_object_or_404(User, id=user_id)
        follower = request.user

        if follower != following:
            follow, created = Follow.objects.get_or_create(follower=follower,
                                                           following=following)

            if created:
                follower.following_count += 1
                follower.save()
                following.follower_count += 1
                following.save()
            else:
                follower.following_count -= 1
                follower.save()
                following.follower_count -= 1
                following.save()
                follow.delete()

        return redirect('profile', user_id=user_id)
