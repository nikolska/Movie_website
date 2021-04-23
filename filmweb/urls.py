"""filmweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path

from movies.views import (
    MovieCreateView, MovieDeleteView, MovieDetailView, MoviesListView, MovieUpdateView,
    PersonCreateView, PersonDeleteView, PersonDetailView, PersonUpdateView, StarsListView
)


urlpatterns = [
    path('', MoviesListView.as_view(), name='movies_list'),
    path('admin/', admin.site.urls, name='admin'),
    re_path(r'^movies/(?P<pk>\d+)/$', MovieDetailView.as_view(), name='movie_details'),
    path('movies/add/', MovieCreateView.as_view(), name='add_movie'),
    re_path(r'^movies/delete/(?P<pk>\d+)/$', MovieDeleteView.as_view(), name='del_movie'),
    re_path(r'^movies/edit/(?P<pk>\d+)/$', MovieUpdateView.as_view(), name='movie_edit'),
    path('stars/', StarsListView.as_view(), name='stars_list'),
    re_path(r'^stars/(?P<pk>\d+)/$', PersonDetailView.as_view(), name='person_details'),
    path('stars/add/', PersonCreateView.as_view(), name='add_person'),
    re_path(r'^stars/delete/(?P<pk>\d+)/$', PersonDeleteView.as_view(), name='del_person'),
    re_path(r'^stars/edit/(?P<pk>\d+)/$', PersonUpdateView.as_view(), name='edit_person'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
