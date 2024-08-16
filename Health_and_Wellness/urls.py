"""
URL configuration for Health_and_Wellness project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings  
from django.conf.urls.static import static 

from web.views import Registration_View
from web.views import Home_View
from web.views import Update_UserProfile_View
from web.views import Login_View
from web.views import Logout_View
from web.views import Profile_View
from web.views import Add_Food
from web.views import Update_food
from web.views import Delete_Food
from web.views import Add_Exercise
from web.views import ExerciseList_View
from web.views import ExerciseDetail_View
from web.views import ExerciseDelete_View
from web.views import ExerciseUpdate_View

urlpatterns = [

    path('',Home_View.as_view(),name='home'),
    path('reg/', Registration_View.as_view(),name='reg'),
    path('upuser/<int:pk>', Update_UserProfile_View.as_view(),name='upuser'),
    path('login/', Login_View.as_view(),name='login'),
    path('logout/', Logout_View.as_view(),name='logout'),
    path('profile/', Profile_View.as_view(),name='profile'),
    path('addfood/',Add_Food.as_view(),name='addfood'),
    path('updatefood/<int:pk>',Update_food.as_view(),name='updatefood'),
    path('deletefood/<int:pk>',Delete_Food.as_view(),name='deletefood'),
    path('addexercise/',Add_Exercise.as_view(),name='addexercise'),
    path('exerciselist/',ExerciseList_View.as_view(),name='exerciselist'),
    path('exerciseview/<int:pk>',ExerciseDetail_View.as_view(),name='exerciseview'),
    path('exercisedelete/<int:pk>',ExerciseDelete_View.as_view(),name='exercisedelete'),
    path('exerciseupdate/<int:pk>',ExerciseUpdate_View.as_view(),name='exerciseUpdate'),
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
