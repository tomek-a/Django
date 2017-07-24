from django.conf.urls import url
from .views import BaseGwentView, LogoutView, LoginView, CreateUserView,\
    CardsView, CardView, ArticlesView, ArticleView, BlogsView, BlogView, DeckBuilderView, DeckBuilderFactionView

urlpatterns = [
    url(r'^deck_builder/(?P<faction>(\w+))', DeckBuilderFactionView.as_view(), name='gwent_deck_builder'),
    url(r'^deck_builder', DeckBuilderView.as_view(), name='gwent_deck_builder_choice'),
    url(r'^blog/(?P<blog_id>(\d)+)', BlogView.as_view(), name='gwent_blog'),
    url(r'^blogs', BlogsView.as_view(), name='gwent_blogs'),
    url(r'^article/(?P<article_id>(\d)+)', ArticleView.as_view(), name='gwent_article'),
    url(r'^articles', ArticlesView.as_view(), name='gwent_articles'),
    url(r'^card/(?P<card_id>(\d)+)', CardView.as_view(), name='gwent_card'),
    url(r'^cards', CardsView.as_view(), name='gwent_cards'),
    url(r'^login', LoginView.as_view(), name='gwent_login'),
    url(r'^logout', LogoutView.as_view(), name='gwent_logout'),
    url(r'^create_user', CreateUserView.as_view(), name='gwent_create_user'),
    url(r'^', BaseGwentView.as_view(), name='gwent_base'),



]