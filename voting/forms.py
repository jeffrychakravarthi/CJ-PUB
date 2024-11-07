from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Candidate, Vote

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['candidate']
        widgets = {'candidate': forms.RadioSelect()}
