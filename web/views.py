from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import login, logout,authenticate

from web.forms import Registration_Form
from web.forms import UserProfile_Form
from web.forms import Login_Form
from web.forms import BMRForm
from web.forms import FoodForm

from web.models import User
from web.models import UserProfile_Model
from web.models import Foods

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
            if gender == 'male':
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
            height_in_meters = height / 100  # convert cm to meters
            bmi = weight / (height_in_meters ** 2)

        return render(request, 'index.html', {'form': form, 'bmr': bmr,'bmi': bmi})
    
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
        # data=UserProfile_Model.objects.get(user_id=request.user)
        # height = data.height
        # weight = data.weight
        # age = data.age
        # gender = data.gender
        # bmr = None
        # bmi = None
        # if gender == 'male':
        #     bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        # else:
        #     bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
        # height_in_meters = height / 100  # convert cm to meters
        # bmi = weight / (height_in_meters ** 2)
        return render(request,'profile.html')


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