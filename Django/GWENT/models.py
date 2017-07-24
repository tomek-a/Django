from django.db import models
from django.contrib.auth.models import User


ARTICLE_TYPE = (
    (1, 'General'),
    (2, 'Strategy'),
    (3, 'DeckTech'),
    (4, 'Competetive')
)


class Article(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User)
    type = models.IntegerField(choices=ARTICLE_TYPE, default=1)
    ranking = models.IntegerField(default=0)

    def show_type(self):
        article_type = dict(ARTICLE_TYPE)[self.type]
        return article_type

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(max_length=160)
    author = models.ForeignKey(User)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ranking = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.author, self.article)


class Blog(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=256)
    date_added = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User)

    def __str__(self):
        return '{} - {}'.format(self.title, self.author)


class Card(models.Model):
    name = models.CharField(max_length=64)
    faction = models.CharField(max_length=64)
    card_set = models.CharField(max_length=64)
    text = models.TextField()
    type = models.CharField(max_length=64)
    rarity = models.CharField(max_length=64)
    flavor = models.TextField()
    strength = models.CharField(max_length=64)
    artist = models.CharField(max_length=64)
    craft_normal = models.PositiveIntegerField()
    craft_premium = models.PositiveIntegerField()
    mill_normal = models.PositiveIntegerField()
    mill_premium = models.PositiveIntegerField()
    thumbnail_link = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Deck(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    ranking = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    creation_date = models.DateField(auto_now_add=True)
    cards = models.ManyToManyField(Card, through='Amount')

    def __str__(self):
        return self.name


class Amount(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    amount = models.IntegerField()



