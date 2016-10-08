from django.conf.urls import include, url
from django.contrib import admin

from .apps.core import views as core

urlpatterns = [
    url(r'^$', core.index_view, name='index'),
    url(r'^admin/', include(admin.site.urls)),
]
