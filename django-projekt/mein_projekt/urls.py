"""
URL configuration for mein_projekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from meine_app import views
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('events', views.events, name='events'),
    path('events/<int:pk>/', views.events_detail, name='events_detail'),
	path('events/new/', views.events_new, name='events_new'),
	path('events/<int:pk>/edit/', views.events_edit, name='events_edit'),
	path('events/<int:pk>/comment/', views.add_comment_to_events, name='add_comment_to_events'),
	path("accounts/", include("accounts.urls")),
	path('accounts/', include("django.contrib.auth.urls")),
	path("", TemplateView.as_view(template_name="home.html"), name="home"),
	path('post', views.post_list, name='post_list'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/new/', views.post_new, name='post_new'), 
	path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),	
	path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
        path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
	path('post/<int:pk>/upvote/', views.vote_up, name='vote_up'),
        path('post/<int:pk>/downvote/', views.vote_down, name='vote_down'),
	path('events/<int:pk>/upvote/', views.events_vote_up, name='events_vote_up'),
		path('events/<int:pk>/downvote/', views.events_vote_down, name='events_vote_down'),        
		path('profil/likes/', views.meine_likes, name='meine_likes'),
		path('profil/', views.profil_view, name='profil'),
		path('meine-events/', views.meine_events, name='meine_events'),
	path('report_jpg', views.report_jpg, name='report_jpg'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)