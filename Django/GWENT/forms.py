from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='E-mail')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class AddCommentForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea)


