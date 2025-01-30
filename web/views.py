from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import login, logout,authenticate
from datetime import timedelta
from django.db.models.functions import TruncWeek,TruncDay
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum

from web.forms import Registration_Form
from web.forms import UserProfile_Form
from web.forms import Login_Form
from web.forms import BMRForm
from web.forms import FoodForm
from web.forms import Exercise_Form
from web.forms import UserFoodForm
from web.forms import SleepForm
from web.forms import DateRangeForm
from web.forms import Userfood_Daterange
from web.forms import Consultant_Form
from web.forms import Food_Goal_Form


from web.models import SleepModel
from web.models import User
from web.models import UserProfile_Model
from web.models import Foods
from web.models import Exercise
from web.models import Exercise_Data
from web.models import UserFood
from web.models import Consultant
from web.models import Food_Goal
from web.models import Exercise_Goal


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
                state='You are Underweight'
            elif 18.5 <= bmi <= 24.9:
                state='You are Normal weight'
            elif 25 <= bmi <= 39.9:
                state=' You are Overweight'
            else:
                state='You are Obese'

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
        return render(request, 'profile_update.html', {'form': form,'data':data})
    
    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        data=UserProfile_Model.objects.get(id=id)
        form = UserProfile_Form(request.POST,request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = UserProfile_Form(instance=data)
            return render(request, 'profile_update.html', {'form': form,'data':data})
        
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

        user_obj=UserProfile_Model.objects.get(user_id=request.user.id)

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
            return render(request,'profile.html',{'data':data,'bmr':bmr,'bmi':bmi,'state':state,"user_obj":user_obj})



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

        userdata=UserProfile_Model.objects.get(user_id=request.user)

        user_obj=UserProfile_Model.objects.get(user_id=request.user.id)

        return render(request,'exerciselist.html',{'exercises':data,"user_obj":user_obj,"userdata":userdata})

class ExerciseDetail_View(View):

    def get (self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Exercise.objects.get(id=id)
        userdata=UserProfile_Model.objects.get(user_id=request.user)
        user_obj=UserProfile_Model.objects.get(user_id=request.user.id)
        return render(request,'exercise_detail.html',{'exercise':data,"user_obj":user_obj,"userdata":userdata})
    
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
        userdata=UserProfile_Model.objects.get(user_id=request.user)
        user_obj=UserProfile_Model.objects.get(user_id=request.user.id)
        return render(request,'exercise_detail.html',{'exercise':data,"user_obj":user_obj,"userdata":userdata})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Exercise.objects.get(id=id)
        Exercise_Data.objects.create(exercise=data,user=request.user)
        return redirect('exerciselist')
    
    


class Add_Sleep(View):

    def get(self,request,*args,**kwargs):

        form=SleepForm()
        
        current_week_start = timezone.now().date() - timezone.timedelta(days=timezone.now().date().weekday())

        data=SleepModel.objects.annotate(week=TruncWeek("sleep_start_time")).filter(user=request.user,week=current_week_start).order_by("week","sleep_start_time")

        
        user_obj=UserProfile_Model.objects.get(user_id=request.user.id)
        

        return render(request,"sleep.html",{"form":form,"data":data,'user_obj':user_obj})
    

    def post(self,request,*args,**kwargs):

        form=SleepForm(request.POST)

        if form.is_valid():

            SleepModel.objects.create(**form.cleaned_data,user=request.user)
        
        current_week_start = timezone.now().date() - timezone.timedelta(days=timezone.now().date().weekday())

        data=SleepModel.objects.annotate(week=TruncWeek("sleep_start_time")).filter(user=request.user,week=current_week_start).order_by("week","sleep_start_time")

        user_obj=UserProfile_Model.objects.get(user_id=request.user.id)

        form=SleepForm()

        return render(request,"sleep.html",{"form":form,"data":data,"user_obj":user_obj})
    

class UpdateSleep(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        data=SleepModel.objects.get(id=id)

        instance={"sleep_start_time":data.sleep_start_time,"sleep_end_time":data.sleep_end_time,"notes":data.notes}

        form=SleepForm(initial=instance)

        current_week_start = timezone.now().date() - timezone.timedelta(days=timezone.now().date().weekday())

        data=SleepModel.objects.annotate(week=TruncWeek("sleep_start_time")).filter(user=request.user,week=current_week_start).order_by("week","sleep_start_time")

        user_obj=UserProfile_Model.objects.get(user_id=request.user.id)

        return render(request,"sleep.html",{"form":form,"data":data,"user_obj":user_obj})
    
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


class Add_Userfood(View):
    def get(self,request,*args,**kwargs):
        form=UserFoodForm()
        datas=UserFood.objects.filter(user=request.user)
        return render(request,"foodcalorie.html",{"form":form,"datas":datas})
    
    def post(self,request,*args,**kwargs):
        form=UserFoodForm(request.POST)
        if form.is_valid():
            food=form.cleaned_data["food"]
            quantity=form.cleaned_data["quantity"]
            calorie=food.calorie
            print(calorie)
            total_calorie=quantity*calorie
            UserFood.objects.create(**form.cleaned_data,user=request.user,total_calories=total_calorie)
            form=UserFoodForm()
            datas=UserFood.objects.filter(user=request.user)
            return render(request,"foodcalorie.html",{"form":form,"datas":datas})
        else:
            print("thankuuu")
        
            
class Update_userfood(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=UserFood.objects.get(id=id)
        form=UserFoodForm(instance=data)
        datas=UserFood.objects.filter(user=request.user)
        return render(request,"foodcalorie.html",{"form":form , "datas":datas })
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=UserFood.objects.get(id=id)
        form=UserFoodForm(request.POST,instance=data)
        if form.is_valid():
            data.food=form.cleaned_data["food"]
            data.quantity=form.cleaned_data["quantity"]
            id=data.food.id
            food_obj=Foods.objects.get(id=id)
            data.total_calories=food_obj.calorie*data.quantity
            data.save()
            datas=UserFood.objects.filter(user=request.user)
            form=UserFoodForm() 
            return render(request,"foodcalorie.html",{"form":form , "datas":datas})
        else:
            print("not updated")


class Delete_userfood(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        UserFood.objects.get(id=id).delete()
        return redirect ("add_userfood")   
            

class Create_foodbyuser(View):
    def get(self,request,*args,**kwargs):
        form=FoodForm()
        return render (request,"createfood.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_userfood")


class ExerciseSummary(View):
    def get(self,request,*args,**kwargs):

        todays_calorie=0
        todays_data = Exercise_Data.objects.filter(user=request.user,created_date=timezone.now().date())
        for calorie in todays_data:
            todays_calorie=todays_calorie+calorie.exercise.calories_burned

        form=DateRangeForm()
        return render(request,'ex_summary.html',{'form':form,'todaysummary': todays_data,'today_calorie':todays_calorie})
    
    def post(self,request,*args,**kwargs):
        form=DateRangeForm(request.POST)
        if form.is_valid():
            start_date=form.cleaned_data['start_date']
            end_date=form.cleaned_data['end_date']
        
        todays_calorie=0
        todays_data = Exercise_Data.objects.filter(user=request.user,created_date=timezone.now().date())
        for calorie in todays_data:
            todays_calorie=todays_calorie+calorie.exercise.calories_burned
        

        dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        
        total_calorie=0
        overall_data = Exercise_Data.objects.filter(user=request.user,created_date__range=[start_date, end_date])
        for calorie in overall_data:
            total_calorie=total_calorie+calorie.exercise.calories_burned
            
        form=DateRangeForm()
        return render(request,'ex_summary.html',{'form':form,'summary': overall_data,'dates':dates,'total_calorie':total_calorie,'todaysummary': todays_data,'today_calorie':todays_calorie})


class Summary_Userfood(View):
    def get(self,request,*args,**kwargs):
        today = timezone.now().date()
        datas=UserFood.objects.annotate(day=TruncDay("created_date")).filter(user=request.user,day=today).order_by("day","created_date")
        totalcalorie_today=0
        for calorie in datas :
            totalcalorie_today += calorie.total_calories
        form=Userfood_Daterange() 
        return render(request,"foodsummary.html",{'datas':datas , "totalcalorie_today":totalcalorie_today , "form":form})
    
    def post(self,request,*args,**kwargs):
        form=Userfood_Daterange(request.POST)
        if form.is_valid():
            start_date=form.cleaned_data['start']
            end_date=form.cleaned_data['end']
            
        today = timezone.now().date()
        datas=UserFood.objects.annotate(day=TruncDay("created_date")).filter(user=request.user,day=today).order_by("day","created_date")
        totalcalorie_today=0
        for calorie in datas :
            totalcalorie_today += calorie.total_calories
        
        data_range = UserFood.objects.filter(user=request.user,created_date__range=[start_date, end_date+timedelta(days=1)])
        total_calorie_range=0
        for calorie in data_range:
            total_calorie_range += calorie.total_calories
            
        form=Userfood_Daterange()    
        return render(request,"foodsummary.html",{'form':form  , "data_range":data_range , "datas":datas , "totalcalorie_today":totalcalorie_today , "total_calorie_range":total_calorie_range })
    
class Consultant_Add_View(View):
    def get(self,request,*args,**kwargs):
        form=Consultant_Form()
        return render(request,'consultant.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=Consultant_Form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            form=Consultant_Form()
            return render(request,'consultant.html',{'form':form})

class Consultant_Update_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Consultant.objects.get(id=id)
        form=Consultant_Form(instance=data)
        return render(request,'consultant.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Consultant.objects.get(id=id)
        form=Consultant_Form(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            form=Consultant_Form()
            return render(request,'consultant.html',{'form':form})

class Consultant_List_View(View):
    def get(self,request,*args,**kwargs):
        data=Consultant.objects.all()
        return render(request,'consultant_list.html',{'data':data})
    

class Food_Goal_Add_View(View):
    def get(self, request, *args, **kwargs):
        form = Food_Goal_Form()
        today = timezone.now().date()
        
        # Initialize goals to None to prevent UnboundLocalError
        goals = None  

        try:
            goals = Food_Goal.objects.get(user=request.user, created_date=today)
        except Food_Goal.DoesNotExist:
            goals = None  # Set it explicitly

        datas = UserFood.objects.annotate(day=TruncDay("created_date")).filter(
            user=request.user, day=today
        ).order_by("day", "created_date")

        totalcalorie_today = sum(calorie.total_calories for calorie in datas)

        return render(
            request, "food_goal.html",
            {"form": form, "datas": datas, "totalcalorie_today": totalcalorie_today, "goals": goals}
        )

    def post(self, request, *args, **kwargs):
        form = Food_Goal_Form(request.POST)
        today = timezone.now().date()
        
        # Check if a goal already exists
        existing_goal = Food_Goal.objects.filter(user=request.user, created_date=today).first()
        if existing_goal:
            messages.error(request, "Already, you have set a goal today.")  
            return redirect("food_goal")  

        if form.is_valid():
            # Create new goal
            new_goal = Food_Goal.objects.create(
                user=request.user,
                goal=form.cleaned_data['goal'],
                created_date=today
            )
            
            messages.success(request, "Goal set successfully!")  
            return redirect("food_goal")  

        # If form is invalid, re-render the page with errors
        datas = UserFood.objects.annotate(day=TruncDay("created_date")).filter(
            user=request.user, day=today
        ).order_by("day", "created_date")

        totalcalorie_today = sum(calorie.total_calories for calorie in datas)

        return render(
            request, "food_goal.html",
            {"form": form, "datas": datas, "totalcalorie_today": totalcalorie_today}
        )
    
class Add_Userfood(View):
    def get(self,request,*args,**kwargs):
        form=UserFoodForm()
        datas=UserFood.objects.filter(user=request.user)
        return render(request,"foodcalorie.html",{"form":form,"datas":datas})
    
    def post(self,request,*args,**kwargs):
        form=UserFoodForm(request.POST)
        if form.is_valid():
            food=form.cleaned_data["food"]
            quantity=form.cleaned_data["quantity"]
            calorie=food.calorie
            print(calorie)
            total_calorie=quantity*calorie
            UserFood.objects.create(**form.cleaned_data,user=request.user,total_calories=total_calorie)
            form=UserFoodForm()
            datas=UserFood.objects.filter(user=request.user)
            return render(request,"foodcalorie.html",{"form":form,"datas":datas})
        else:
            print("thankuuu")


class Food_Leaderboard_View(View):
    def get(self, request, *args, **kwargs):
        # Get total calories per user and order by total_calories in descending order
        user_calories = UserFood.objects.values('user__username').annotate(total_calories=Sum('total_calories')).order_by('-total_calories')

        # Assign ranks dynamically (users with same points share the same rank)
        ranked_users = []
        rank = 1
        prev_score = None

        for index, user in enumerate(user_calories):
            if prev_score is not None and user['total_calories'] < prev_score:
                rank = index + 1  # Update rank only if the score changes
            
            ranked_users.append({
                "rank": rank,
                "username": user["user__username"],
                "total_calories": user["total_calories"]
            })
            prev_score = user["total_calories"]

        return render(request, "food_leaderboard.html", {"ranked_users": ranked_users})

class Exercise_Leaderboard_View(View):

    def get(self, request):
        
        users = User.objects.all()
        for user in users:
            total_calories = Exercise_Data.objects.filter(user=user).aggregate(
                total=Sum("exercise__calories_burned")
            )["total"] or 0  # Default to 0 if no exercise data

            # Update or create Exercise_Goal entry for the user
            Exercise_Goal.objects.update_or_create(user=user, defaults={"total_calories": total_calories})

        # Retrieve the top 5 users based on total calories burned
        leaderboard = Exercise_Goal.objects.select_related("user").order_by("-total_calories")[:5]

        return render(request, "exercise_leaderboard.html", {"leaderboard": leaderboard})
    
