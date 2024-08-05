from django.contrib import admin

from webapp.models import Image, Post, Follow

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Follow)
