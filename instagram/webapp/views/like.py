from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from ..models import Post
from ..models import Like


User = get_user_model()


class LikeView(View):
    def post(self, request, post_id):
        user = request.user
        post = get_object_or_404(Post, id=post_id)
        liked = Like.objects.filter(author=user, post=post).exists()

        if liked:
            Like.objects.filter(author=user, post=post).delete()
            post.like_count -= 1
            liked = False
        else:
            Like.objects.create(author=user, post=post)
            post.like_count += 1
            liked = True

        post.save()

        return JsonResponse({'success': True, 'liked': liked, 'like_count': post.like_count})