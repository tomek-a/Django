from django import forms

class AddTweetForm(forms.Form):
    content = forms.CharField(max_length=160, widget=forms.Textarea, label='')

class AddMessageForm(forms.Form):
    title = forms.CharField(label='Title')
    message_to = forms.CharField(label='To')
    content = forms.CharField(label='', widget=forms.Textarea)