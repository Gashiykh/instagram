from django.urls import path
from django.contrib.auth import views as django_views

from accounts import views

from accounts.views import UserProfileUpdateView


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', django_views.LogoutView.as_view(), name='logout'),
    path('edit_profile/', UserProfileUpdateView.as_view(), name='edit_profile'),
]
