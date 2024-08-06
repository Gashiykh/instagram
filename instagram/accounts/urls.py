from django.urls import path
from django.contrib.auth import views as django_views

from accounts import views

urlpatterns = [
    path ('login',  views.login_view, name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('logout', django_views.LogoutView.as_view(), name='logout')
]