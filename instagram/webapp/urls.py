from django.urls import path

from .views import IndexListView, UserSearchView, FollowView

from .views import PostView, PostCreateView, LikeView, CommentCreateView, PostDeleteView 
from .views import UserProfileView


urlpatterns = [
    path('', IndexListView.as_view(), name='home'),
    path('search/', UserSearchView.as_view(), name='search'),
    path(
        'profile/<int:user_id>/',
        UserProfileView.as_view(),
        name='profile'
    ),

    path('follow/<int:user_id>/', FollowView.as_view(), name='follow'),
    path('add_post/', PostCreateView.as_view(), name='add_post'),
    path('post/<int:post_id>/', PostView.as_view(), name='post'),
    path('post/<int:post_id>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('like/<int:post_id>/', LikeView.as_view(), name='like-post'),
    path('posts/<int:post_id>/comment/',
         CommentCreateView.as_view(),
         name='add_comment'),
]
