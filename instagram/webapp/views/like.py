from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from webapp.models import Post
from webapp.models import Like


class LikeView(View):
    def get(self, request, post_id):
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

        return JsonResponse({
            'success': True,
            'liked': liked,
            'like_count': post.like_count
        })
