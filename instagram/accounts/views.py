from urllib.parse import parse_qs, urlparse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth import login

from accounts.forms import MyUserCreationForm, LoginForm
from django.views.generic import UpdateView


class RegisterView(generic.CreateView):
    model = get_user_model()
    template_name = 'accounts/register.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='accounts.backends.EmailOrUsernameModelBackend')
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        next_url = self.request.POST.get('next')
        
        if not next_url:
            next_url = self.request.GET.get('next')
        if not next_url:
            next_url = reverse('home')

        return next_url
        

def login_view(request):
    if request.method == 'POST':
        parsed_uri = urlparse(request.build_absolute_uri())
        query = {key: value[0]
                 for key, value in
                 parse_qs(parsed_uri.query).items()}

        next_url = query.get('next')

        form = LoginForm(request.POST)
        form.request = request  
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)

                if next_url:
                    return redirect(next_url)

                return redirect('home')  
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = MyUserCreationForm
    template_name = 'instagram/edit_profile.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})

    def get_object(self, queryset=None):
        return self.request.user
