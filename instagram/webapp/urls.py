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
]
