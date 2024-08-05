from django.contrib import admin

from webapp.models import Follow, Image, Post


admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Follow)
