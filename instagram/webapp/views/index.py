from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model


class IndexListView(generic.ListView):
    model = get_user_model()
    template_name = 'instagram/home.html'
    context_object_name = 'user_objs'
