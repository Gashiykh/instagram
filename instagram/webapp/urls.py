from django.urls import path

from .views import IndexListView, UserSearchView, UserProfileView, FollowView, LikeView

urlpatterns = [
    path('', IndexListView.as_view(), name='home'),
    path('search/', UserSearchView.as_view(), name='search'),
    path(
        'profile/<int:user_id>/',
        UserProfileView.as_view(),
        name='profile'
    ),
    path('like/<int:post_id>/', LikeView.as_view(), name='like-post'),

]
