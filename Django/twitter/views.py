from django.shortcuts import render
from django.views import View
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Tweet, Message
from .forms import AddTweetForm, AddMessageForm
from django.contrib.auth.models import User


# Create your views here.

class BaseView(View):
    def get(self, request):
        form = AddTweetForm()
        current_user = request.user
        tweet_list = Tweet.objects.all().order_by('-creation_date')
        ctx = {
            'tweet_list': tweet_list,
            'current_user': current_user,
            'form': form
        }

        return TemplateResponse(request, 'tweet_list.html', ctx)

    def post(self, request):
        form = AddTweetForm(request.POST)
        if form.is_valid():
            current_user = request.user
            content = form.cleaned_data['content']
            new_tweet = Tweet.objects.create(content=content, user=current_user)
            tweet_list = Tweet.objects.filter(user__pk=current_user.id).order_by('creation_date')
            ctx = {
                'tweet_list': tweet_list,
                'current_user': current_user,
                'form': form
            }

            return TemplateResponse(request, 'tweet_list.html', ctx)


class TweetView(View):
    def get(self, request, user_name, tweet_id):
        tweet = Tweet.objects.filter(user__username=user_name).get(pk=tweet_id)
        current_user = request.user
        ctx = {
            'tweet': tweet,
            'current_user': current_user
        }
        return TemplateResponse(request, 'tweet_info.html', ctx)


class MessageView(View):
    def get(self, request, user_name):
        current_user = request.user
        messages = Message.objects.filter(message_to=current_user.id)
        form = AddMessageForm()
        ctx = {
            'messages': messages,
            'current_user': current_user,
            'form': form
        }
        return TemplateResponse(request, 'message_list.html', ctx)

    def post(self, request, user_name):
        current_user = request.user
        form = AddMessageForm(request.POST)
        if form.is_valid():
            messages = Message.objects.filter(message_to=current_user.id)
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            message_to = form.cleaned_data['message_to']
            receiver = User.objects.get(email=message_to)
            if (receiver != current_user):
                print(current_user.id)
                new_message = Message.objects.create(
                    title=title,
                    content=content,
                    message_from=current_user,
                    message_to=receiver
                )
                status = 'Message sent!'
            else:
                status = "Can't send message to yourself ;)"
            form = AddMessageForm()
            ctx = {
                'form': form,
                'current_user': current_user,
                'messages': messages,
                'status': status
            }

            return TemplateResponse(request, 'message_list.html', ctx)
