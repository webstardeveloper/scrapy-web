"""SearchDCA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

from django.contrib.auth.views import (logout, login, password_change, password_change_done,
                                        password_reset, password_reset_done,
                                        password_reset_confirm, password_reset_complete)

from app import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Authorization, Registration
    url(r'^login/', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', views.register, name='register'),

    # change password urls
    url(r'^password-change/$', password_change, name='password_change'),
    url(r'^password-change/done/$', password_change_done, name='password_change_done'),

    # restore password urls
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),

    url(r'^search-dca/', views.search_dca, name='search-dca'),
    url(r'^search-florida/', views.search_florida, name='search-florida'),

    url(r'^$', RedirectView.as_view(url='/search-dca/')),
]
