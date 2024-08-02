from django.urls import path

from webapp import views

urlpatterns = [
    path('', views.IndexListView.as_view(), name='home')
]