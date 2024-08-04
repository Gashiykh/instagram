from urllib.parse import urlencode

from django.db.models import Q
from django.views.generic import ListView

from accounts.models import User
from webapp.forms import UserSearchForm


class UserSearchView(ListView):
    context_object_name = 'users'
    model = User
    paginate_by = 10
    template_name = 'instagram/users_list.html'

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_string = self.get_search_string()
        print(self.search_string)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form

        if self.search_string:
            context['query'] = urlencode({'search_string': self.search_string})

        return context

    def get_queryset(self):
        filter_query = (
                Q(username__icontains=self.search_string) |
                Q(email__icontains=self.search_string) |
                Q(first_name__icontains=self.search_string) |
                Q(last_name__icontains=self.search_string)
        )
        qs = self.model.objects.filter(filter_query)

        return qs

    def get_search_form(self):
        return UserSearchForm(self.request.GET)

    def get_search_string(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search_string')
