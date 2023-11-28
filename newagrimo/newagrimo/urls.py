
from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signup', views.signupsystem, name='signupsystem'),
    path('login', views.loginsystem, name='loginsystem'),
    path('logout', views.logoutsystem, name='logoutsystem'),
    path('lessons', views.lessons, name='lessons'),
    path('bots', views.bots, name='bots'),
    path('profileo', views.profileo, name='po'),
    path('compvision', views.compvision, name='compvision'),
    path('create_story', views.create_story, name='create_story'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
