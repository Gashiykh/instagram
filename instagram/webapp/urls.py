from django.urls import path

from webapp import views


urlpatterns = [
    path('', views.IndexListView.as_view(), name='home'),
    path('search/', views.UserSearchView.as_view(), name='search'),
    path(
        'profile/<int:user_id>/',
        views.UserProfileView.as_view(),
        name='profile'
    ),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow'),
    path('add_post', views.PostCreateView.as_view(), name='add_post'),
    path('posts', views.PostListView.as_view(), name='posts'),
]
