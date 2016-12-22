from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'quiz.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^lists-page/$', views.detail, name='detail'),
    url(r'^table-page/$', views.table, name='table'),
    url(r'^charts-page/$', views.charts, name='charts'),
]
