from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='E-mail')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class AddCommentForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea)

class CreateUserForm(forms.Form):
    username = forms.CharField(label='Username')
    email = forms.CharField(label='E-mail')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)