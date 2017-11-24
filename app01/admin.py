from django.contrib import admin
from app01 import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Info)
admin.site.register(models.Article)
admin.site.register(models.Article2tag)
admin.site.register(models.Article_detail)
admin.site.register(models.Article_poll)
admin.site.register(models.Blog)
admin.site.register(models.Classfication)
admin.site.register(models.Comment)
admin.site.register(models.Comment_poll)
admin.site.register(models.Web_class)
admin.site.register(models.Web_artile_cla)
admin.site.register(models.Tag)