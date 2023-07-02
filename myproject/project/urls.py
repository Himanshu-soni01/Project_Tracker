from django.contrib import admin
from django.urls import path
from project import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.index,name="admin"),
    path("Users/",views.users,name="Users"),
    path("CreateProject/",views.CreateProject,name='admin_portal'),
    path("userlogin/",views.userlogin,name='Login'),
    path("usersignup",views.usersignup,name="SignUp"),
    path("logout/",views.logout,name="logout"),
    path("Projects/",views.projects,name="Projects"),
    path('download_file/<path:file_path>/', views.download_file, name='download_file'),
    
    path('update_project/<str:project_name>/', views.update_project, name='update_project'),


    # path("afterlogin/",views),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
