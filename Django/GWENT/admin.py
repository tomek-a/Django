from django.contrib import admin
from . import models


#ADMIN STUDENT
admin.site.register(models.Article)
admin.site.register(models.Blog)