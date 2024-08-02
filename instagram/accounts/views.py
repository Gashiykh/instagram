from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth import login

from accounts.forms import MyUserCreationForm


class RegisterView(generic.CreateView):
    model = get_user_model()
    template_name = 'accounts/register.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        next_url = self.request.POST.get('next')
        
        if not next_url:
            next_url = self.request.GET.get('next')
        if not next_url:
            next_url = reverse('home')

        return next_url
        

