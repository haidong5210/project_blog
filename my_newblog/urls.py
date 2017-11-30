
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^$', views.index),
    url(r'^cate/(?P<cate>.*)/$', views.index),
    url(r'^reg/$', views.reg),

    url(r'^poll/$', views.poll),
    url(r'^del/$', views.dell),
    url(r'^test/(?P<article_id>\d+)$', views.test),

    url(r'^login/$', views.login),
    url(r'^img/', views.img),
    url(r'^article_img/', views.article_img),
    url(r'^logout/$', views.logout),
    url(r'^pc-geetest/ajax_validate',views.pcajax_validate, name='pcajax_validate'),
    url(r'^pc-geetest/register', views.pcgetcaptcha, name='pcgetcaptcha'),

    url(r'^blog/', include('app01.urls')),
    url(r'^comment/', views.comment),
    # media 配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]