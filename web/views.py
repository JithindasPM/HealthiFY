from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import login, logout,authenticate

from web.forms import Registration_Form
from web.forms import UserProfile_Form
from web.forms import Login_Form
from web.forms import BMRForm
from web.forms import FoodForm
from web.forms import Exercise_Form
from .forms import SleepForm
from .models import SleepModel

from web.models import User
from web.models import UserProfile_Model
from web.models import Foods
from web.models import Exercise
from web.models import Exercise_Data


from django.db.models.functions import TruncWeek
from django.utils import timezone


# Create your views here.

class Home_View(View):
    def get(self,request,*args,**kwargs):
        form=BMRForm()
        return render(request,'index.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=BMRForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            bmr = None
            bmi = None
            state=None
            if gender == 'male':
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
            height_in_meters = height / 100  # convert cm to meters
            bmi = weight / (height_in_meters ** 2)
            if bmi is None:
                state=None
            elif bmi <= 18.4:
                state='Underweight'
            elif 18.5 <= bmi <= 24.9:
                state='Normal weight'
            elif 25 <= bmi <= 39.9:
                state='Overweight'
            else:
                state='Obese'

        return render(request, 'index.html', {'form': form, 'bmr': bmr,'bmi': bmi,'state':state})
    
class Registration_View(View):
    def get(self,request,*args,**kwargs):
        form=Registration_Form()
        return render(request,'reg.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=Registration_Form(request.POST)
        try:
            if form.is_valid():
               User.objects.create_user(**form.cleaned_data)
               form=Registration_Form()
               return redirect('login')
        except Exception as e:
            print(e,"===========")
        return render(request,'reg.html',{'form':form})
        
class Update_UserProfile_View(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        data=UserProfile_Model.objects.get(id=id)
        form = UserProfile_Form(instance=data)
        return render(request, 'profile_update.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        data=UserProfile_Model.objects.get(id=id)
        form = UserProfile_Form(request.POST,request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = UserProfile_Form(instance=data)
            return render(request, 'profile_update.html', {'form': form})
        
class Login_View(View):
    def get(Self,request,*args,**kwargs):
        form=Login_Form()
        return render(request,'login.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=Login_Form(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get('username')
            pswd=form.cleaned_data.get('password')

            user_obj=authenticate(username=u_name,password=pswd)
            if user_obj:
                login(request,user_obj)
                user_obj=UserProfile_Model.objects.get(user=request.user)
                if user_obj.age is None or user_obj.height is None or user_obj.weight is None or user_obj.gender is None:
                    id=user_obj.id 
                    return redirect('upuser',pk=id)
                else:
                    return redirect('profile')
            else:
                form=Login_Form()
                return render(request,'login.html',{'form':form})  

            
class Logout_View(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('home')
    
class Profile_View(View):
    def get(self,request,*args,**kwargs):
        data=UserProfile_Model.objects.get(user_id=request.user)
        height = data.height
        weight = data.weight
        age = data.age
        gender = data.gender

        if height is None or weight is None or age is None:
            return render(request,'profile.html',{'data':data})
        else:
            height = float(height)
            weight = float(weight)
            age = int(age)
            bmr = None
            bmi = None
            state=None
            if gender == 'male':
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

            height_in_meters = height / 100  # convert cm to meters
            bmi = weight / (height_in_meters ** 2)
            if bmi is None:
                state=None
            elif bmi <= 18.4:
                state='Underweight'
            elif 18.5 <= bmi <= 24.9:
                state='Normal weight'
            elif 25 <= bmi <= 39.9:
                state='Overweight'
            else:
                state='Obese'
            return render(request,'profile.html',{'data':data,'bmr':bmr,'bmi':bmi,'state':state})



class Add_Food(View):
    def get(self,request,*args,**kwargs):
        form=FoodForm
        data=Foods.objects.all()
        return render(request,"food.html",{"form":form,'data':data})
    
    def post(self,request,*args,**kwargs):
        form=FoodForm(request.POST)
        if form.is_valid():
            form.save()
            form=FoodForm()
        data=Foods.objects.all()
        return render(request,"food.html",{"form":form,"data":data})
    
class Update_food(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Foods.objects.get(id=id)
        form=FoodForm(instance=data)
        data=Foods.objects.all()
        return render(request,"food.html",{"form":form,"data":data})
        
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Foods.objects.get(id=id)
        form=FoodForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect("addfood")


class Delete_Food(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Foods.objects.get(id=id).delete()
        return redirect("addfood")

class Add_Exercise(View):

    def get(self,request,*args,**kwargs):
        form=Exercise_Form()
        return render(request,'exercise.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=Exercise_Form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        form=Exercise_Form()
        return render(request,'exercise.html',{'form':form})


class ExerciseList_View(View):

    def get(self,request,*args,**kwargs):

        data=Exercise.objects.all()

        return render(request,'exerciselist.html',{'exercises':data})

class ExerciseDetail_View(View):

    def get (self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Exercise.objects.get(id=id)

        return render(request,'exercise_detail.html',{'exercise':data})
    
class ExerciseDelete_View(View):
    def get(sel,request,*args,**kwargs):
        id=kwargs.get('pk')
        Exercise.objects.get(id=id).delete()
        return redirect('exerciselist')
    
class ExerciseUpdate_View(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Exercise.objects.get(id=id)
        form=Exercise_Form(instance=data)

        return render(request,'exercise.html',{'form':form,'data':data})
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Exercise.objects.get(id=id)
        form=Exercise_Form(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
        form=Exercise_Form()
        return render(request,'exercise.html',{'form':form})
    

class ExerciseData_view(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Exercise.objects.get(id=id)
        return render(request,'exercise_detail.html',{'exercise':data})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Exercise.objects.get(id=id)
        Exercise_Data.objects.create(exercise=data,user=request.user)
        return redirect('exerciselist')
    
    


class Add_Sleep(View):

    def get(self,request,*args,**kwargs):

        form=SleepForm()

        current_week_start = timezone.now().date() - timezone.timedelta(days=timezone.now().date().weekday())

        data=SleepModel.objects.annotate(week=TruncWeek("sleep_start_time")).filter(week=current_week_start).order_by("week","sleep_start_time")

        return render(request,"sleep.html",{"form":form,"data":data})
    

    def post(self,request,*args,**kwargs):

        form=SleepForm(request.POST)

        if form.is_valid():

            SleepModel.objects.create(**form.cleaned_data,user=request.user)
        
        current_week_start = timezone.now().date() - timezone.timedelta(days=timezone.now().date().weekday())

        data=SleepModel.objects.annotate(week=TruncWeek("sleep_start_time")).filter(week=current_week_start).order_by("week","sleep_start_time")

        form=SleepForm()

        return render(request,"sleep.html",{"form":form,"data":data})
    

class UpdateSleep(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        data=SleepModel.objects.get(id=id)

        instance={"sleep_start_time":data.sleep_start_time,"sleep_end_time":data.sleep_end_time,"notes":data.notes}

        form=SleepForm(initial=instance)

        all_data=SleepModel.objects.all()

        return render(request,"sleep.html",{"form":form,"data":all_data})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        data=SleepModel.objects.get(id=id)

        form=SleepForm(request.POST,initial=data)

        if form.is_valid():

            data.sleep_start_time=form.cleaned_data["sleep_start_time"]

            data.sleep_end_time=form.cleaned_data["sleep_end_time"]

            data.notes=form.cleaned_data["notes"]

            data.save()

        return redirect("addsleep")
    

class DeleteSleep(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        SleepModel.objects.get(id=id).delete()

        return redirect("addsleep")



