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
        type = dict(ARTICLE_TYPE)[self.type]
        return type

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
