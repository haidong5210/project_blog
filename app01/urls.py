from django.conf.urls import url
from app01 import views
urlpatterns = [
    url(r'^del_article/$',views.del_article),
    url(r'^addArticle/$',views.addArticle),
    url(r'^cnblogs/$',views.cnblog),
    url(r'^cnblogs/(\d+)/$',views.edit_article),
    url(r'^(?P<username>.*)/(?P<leibie>tag|category|archive)/(?P<canshu>.*)/$', views.homeSite),
    url(r'^(?P<username>.*)/p/(?P<id>.*)/$', views.article),
    url(r'^(?P<username>.*)/$', views.homeSite),
]