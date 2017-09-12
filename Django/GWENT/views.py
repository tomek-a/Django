from django.shortcuts import render
import json
import urllib.request
from urllib.request import Request, urlopen
#RESPONSES
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
#FORMS
from .forms import LoginForm, AddCommentForm, CreateUserForm
#MODELS, VIEWS
from django.contrib.auth.models import User
from .models import Article, Comment, Blog, Card
from django.views import View
#AUTHENTICATION
from django.contrib.auth import authenticate, login, logout
#PAGINATION
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#Q QUERY
from django.db.models import Q
#---------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------
class BaseGwentView(View):
    def get(self, request):
        article_query = Article.objects.all().order_by('date_added')
        blog_query = Blog.objects.all().order_by('date_added')
        content_list = []
        #functions changing query object to dictionary
        def getArt(article):
            return {
                'title': article.title,
                'type': article.show_type(),
                'author': article.author,
                'ranking': article.ranking,
                'date_added': article.date_added,
                'id': article.pk,
                'kind': 'article'
            }
        def getBlog(blog):
            return {
                'title': blog.title,
                'type': 'Blog post',
                'author': blog.author,
                'ranking': 0,
                'date_added': blog.date_added,
                'id': blog.pk,
                'kind': 'blog'

            }
        #making content_list
        content_amount = 10
        i = len(article_query)-1 #matching list indexes
        y = len(blog_query)-1
        if i >= 0 or y >= 0:
            for c_a in range(content_amount):
                print(i)
                print(y)
                if (y != -1 and i != -1):
                    if getArt(article_query[i])['date_added'] <= getBlog(blog_query[y])['date_added']:
                        content_list.append(getBlog(blog_query[y]))
                        y -= 1
                    else:
                        content_list.append(getArt(article_query[i]))
                        i -= 1
                elif y == -1:
                    content_list.append(getArt(article_query[i]))
                    i -= 1
                    if i == -1:
                        break
                elif i == -1:
                    content_list.append(getBlog(blog_query[y]))
                    y -= 1
                    if y == -1:
                        break
                else:
                    break
        ctx = {
            'content_list': content_list
        }
        return TemplateResponse(request, 'GWENT/index.html', ctx)
#---------------------------------------------------------------------------------------------------------------------
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/GWENT')
#---------------------------------------------------------------------------------------------------------------------
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'GWENT/login.html', ctx)

    def post(self, request):
        user = None
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                username = User.objects.get(email=email)
                user = authenticate(username=username, password=password)
            except:
                pass
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/GWENT')
        else:
            form = LoginForm()
            error = 'WRONG LOGIN/PASSWORD'
            ctx = {
                'form': form,
                'error': error
            }
            return TemplateResponse(request, 'GWENT/login.html', ctx)
#---------------------------------------------------------------------------------------------------------------------
class CreateUserView(View):
    def get(self, request):
        form = CreateUserForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'GWENT/create_user.html', ctx)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            emails = []
            usernames = []
            users = User.objects.all()
            for user in users:
                emails.append(user.email)
            for user in users:
                usernames.append(user.username)
            if email in emails or username in usernames:
                error = 'EMAIL/USERNAME ALREADY IN USE, PLEASE TRY ANOTHER'
                ctx = {
                    'form': form,
                    'error': error
                }
                return TemplateResponse(request, 'GWENT/create_user.html', ctx)
            else:
                User.objects.create_user(username=username, password=password, email=email)
                return HttpResponseRedirect('/GWENT/login')

#---------------------------------------------------------------------------------------------------------------------
class CardsView(View):
    def get(self, request):
        card_list = Card.objects.all()
        paginator = Paginator(card_list, 20)
        page = request.GET.get('page')
        page_num = paginator.num_pages
        try:
            cards = paginator.page(page)
        except PageNotAnInteger:
            cards = paginator.page(1)
        except EmptyPage:
            cards = paginator.page(paginator.num_pages)
        ctx = {
            'cards': cards,
            'page': page,
            'page_num': range(page_num)
        }
        return TemplateResponse(request, 'GWENT/card_list.html', ctx)
#---------------------------------------------------------------------------------------------------------------------
class CardView(View):
    def get(self, request, card_id):
        card = Card.objects.get(pk=card_id)

        ctx = {
            'card': card
        }
        return TemplateResponse(request, 'GWENT/card.html', ctx)
#---------------------------------------------------------------------------------------------------------------------
class ArticlesView(View):
    def get(self, request):
        article_list = Article.objects.all().order_by('-date_added')
        ctx = {
            'article_list': article_list
        }
        return TemplateResponse(request, 'GWENT/article_list.html', ctx)
#---------------------------------------------------------------------------------------------------------------------
class ArticleView(View):
    def get(self, request, article_id):
        article = Article.objects.get(pk=article_id)
        comments = Comment.objects.filter(article=article_id)
        form = AddCommentForm()

        ctx = {
            'article': article,
            'form': form,
            'comments': comments
        }
        return TemplateResponse(request, 'GWENT/article.html', ctx)

    def post(self, request, article_id):
        form = AddCommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            article = Article.objects.get(pk=article_id)
            Comment.objects.create(
                author = request.user,
                content = content,
                article = article
            )
        return HttpResponseRedirect('/GWENT/article/{}'.format(article_id))
#---------------------------------------------------------------------------------------------------------------------
class BlogsView(View):
    def get(self, request):
        blog_list = Blog.objects.all().order_by('-date_added')
        ctx = {
            'blog_list': blog_list
        }
        return TemplateResponse(request, 'GWENT/blog_list.html', ctx)
#---------------------------------------------------------------------------------------------------------------------
class BlogView(View):
    def get(self, request, blog_id):
        blog = Blog.objects.get(pk=blog_id)
        ctx = {
            'blog': blog
        }
        return TemplateResponse(request, 'GWENT/blog.html', ctx)
#---------------------------------------------------------------------------------------------------------------------
class DeckBuilderView(View):
    def get(self, request):
        monster_leaders = Card.objects.filter(type='Leader', faction='Monster')
        skellige_leaders = Card.objects.filter(type='Leader', faction='Skellige')
        scoiatael_leaders = Card.objects.filter(type='Leader', faction="Scoia'tael")
        northernrealms_leaders = Card.objects.filter(type='Leader', faction='Northern Realms')
        nilfgaard_leaders = Card.objects.filter(type='Leader', faction='Nilfgaard')

        ctx = {
            'monster_leaders': monster_leaders,
            'skellige_leaders': skellige_leaders,
            'scoiatael_leaders': scoiatael_leaders,
            'northernrealms_leaders': northernrealms_leaders,
            'nilfgaard_leaders': nilfgaard_leaders
        }
        return TemplateResponse(request, 'GWENT/deck_builder_choice.html', ctx)


class DeckBuilderFactionView(View):
    def get(self, request, faction):
        if faction == 'scoiatael':
            faction = "Scoia'tael"
        elif faction == 'northernrealms':
            faction = 'Northern Realms'
        cards = Card.objects.filter(
            (Q(faction=faction) | Q(faction='neutral')), ~Q(type='leader')
        )
        leaders = Card.objects.filter(
            Q(faction=faction) & Q(type='leader')
        )
        print(leaders)

        ctx = {
            'cards': cards,
            'leaders': leaders
        }
        return TemplateResponse(request, 'GWENT/deck_builder.html', ctx)














