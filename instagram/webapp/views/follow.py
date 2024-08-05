from django.shortcuts import get_object_or_404, redirect
from django.views import View

from accounts.models import User
from webapp.models import Follow


class FollowView(View):
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

        return redirect('profile', user_id=user_id)