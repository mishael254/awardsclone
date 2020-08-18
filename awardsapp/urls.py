from django.urls import re_path,include,path
from .import views
from django.conf import settings
from django.conf.urls.static import static

# Creating Urls
urlpatterns = [
    re_path('^$',views.home,name='home'),
    re_path(r'^uploads/', views.upload_project, name='uploadproject'),
    re_path(r'^projects/(\d+)',views.projects,name='projects'),
    re_path(r'^profile/(?P<username>\w+)', views.profile, name='profile'),
    re_path(r'^api/profiles/$', views.ProfileList.as_view(),name='profile_list'),
    re_path(r'^api/projects/$', views.ProjectsList.as_view(),name='projects_list'),
    re_path(r'^search/', views.search_results, name='search_results'),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 