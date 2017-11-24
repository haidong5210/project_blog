from django.conf.urls import url
from app01 import views
urlpatterns = [
    url(r'^(?P<username>.*)/(?P<leibie>tag|category|archive)/(?P<canshu>.*)/$', views.homeSite),
    url(r'^(?P<username>.*)/p/(?P<id>.*)/$', views.article),
    url(r'^(?P<username>.*)/$', views.homeSite),
]