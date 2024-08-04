from django import forms


class UserSearchForm(forms.Form):
    search_string = forms.CharField(max_length=100, required=False)
