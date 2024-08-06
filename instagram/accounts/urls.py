from django.urls import path
from django.contrib.auth import views as django_views

from accounts import views

urlpatterns = [
    path ('login', django_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('register', views.RegisterView.as_view(), name='register')

]