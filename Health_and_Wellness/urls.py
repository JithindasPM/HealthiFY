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
from web.views import ExerciseData_view
from web.views import Add_Sleep
from web.views import UpdateSleep
from web.views import DeleteSleep
from web.views import Add_Userfood
from web.views import Update_userfood
from web.views import Delete_userfood
from web.views import Create_foodbyuser
from web.views import ExerciseSummary
from web.views import Summary_Userfood
from web.views import Consultant_Add_View
from web.views import Consultant_List_View
from web.views import Consultant_Update_View
from web.views import Food_Goal_Add_View
from web.views import Food_Leaderboard


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
    path('exercise/<int:pk>/',ExerciseData_view.as_view(),name='finish_exercise'),
    path('addsleep/',Add_Sleep.as_view(),name="addsleep"),
    path('upsleep/<int:pk>/',UpdateSleep.as_view(),name="updatesleep"),
    path('deletesleep/<int:pk>/',DeleteSleep.as_view(),name="deletesleep"),
    path('add_food/', Add_Userfood.as_view(), name='add_userfood'),
    path('update_food/<int:pk>', Update_userfood.as_view(), name='update_food'),
    path('delete_food/<int:pk>', Delete_userfood.as_view(), name='delete_food'),
    path('create_foodbyuser/', Create_foodbyuser.as_view(), name='create_foodbyuser'),
    path('exsummary/', ExerciseSummary.as_view(), name='exsummary'),
    path('food_summary/', Summary_Userfood.as_view(), name='food_summary'),
    path('consultant_add/', Consultant_Add_View.as_view(), name='consultant_add'),
    path('consultant/', Consultant_List_View.as_view(), name='consultant'),
    path('consultant_update/<int:pk>',Consultant_Update_View.as_view(),name='consultant_update'),
    path('food_goal/', Food_Goal_Add_View.as_view(), name='food_goal'),
    path('food_leaderboard/', Food_Leaderboard.as_view(), name='food_leaderboard'),

    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
