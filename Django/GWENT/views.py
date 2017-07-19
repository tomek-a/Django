from django.shortcuts import render
import json
import urllib.request
from urllib.request import Request, urlopen
#RESPONSES
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
#FORMS
from .forms import LoginForm, AddCommentForm
#MODELS, VIEWS
from django.contrib.auth.models import User
from .models import Article, Comment, Blog
from django.views import View
#AUTHENTICATION
from django.contrib.auth import authenticate, login, logout
#---------------------------------------------------------------------------------------------------------------------
#getting card list from GWENTApi
#---------------------------------------------------------------------------------------------------------------------
url_request = Request(
            'https://api.gwentapi.com/v0/cards?limit=305', #actuall card pool size 305
            headers={"User-Agent": "Magic-Browser"}
)
r = urlopen(url_request)
data_ = r.read().decode(r.info().get_param('charset') or 'utf-8')
data = json.loads(str(data_))
card_list = data['results']
#---------------------------------------------------------------------------------------------------------------------
class BaseGwentView(View):
    def get(self, request):
        article_query = Article.objects.all().order_by('date_added')
        blog_query = Blog.objects.all().order_by('date_added')

        article_list = []
        blog_list = []
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
        pass
#---------------------------------------------------------------------------------------------------------------------
class CardsView(View):
    def get(self, request):
        ctx = {
            'card_list': card_list
        }
        return TemplateResponse(request, 'GWENT/card_list.html', ctx)

class CardView(View):
    def get(self, request, card_id):
        card_id = int(card_id) - 1
        card_link = card_list[card_id]['href']

        card_url_request = Request(card_link, headers={"User-Agent": "Magic-Browser"})
        r_card = urlopen(card_url_request)
        card_data_ = r_card.read().decode(r_card.info().get_param('charset') or 'utf-8')
        card_data = json.loads(str(card_data_))
        thumbnail_link_json = card_data['variations'][0]['href']

        thumbnail_url_request = Request(thumbnail_link_json, headers={"User-Agent": "Magic-Browser"})
        r_thumb = urlopen(thumbnail_url_request)
        thumb_data_ = r_thumb.read().decode(r_thumb.info().get_param('charset') or 'utf-8')
        thumbnail = json.loads(str(thumb_data_))
        thumbnail_link = thumbnail['art']['thumbnailImage']



        try:
            strength = card_data['strength']
        except:
            strength = 'None'
        ctx = {
            'name': card_data['name'],
            'faction': card_data['faction']['name'],
            'text': card_data['info'],
            'strength': strength,
            'type': card_data['group']['name'],
            'rarity': card_data['variations'][0]['rarity']['name'],
            'row': ', '.join(card_data['positions']),
            'flavor': card_data['flavor'],
            'thumbnail_link': thumbnail_link
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
            new_comment = Comment.objects.create(
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







