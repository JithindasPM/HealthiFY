from django import forms
from django.contrib.auth.forms import UserCreationForm

from web.models import User
from web.models import UserProfile_Model
from web.models import Foods
from web.models import Exercise
from web.models import UserFood

class Registration_Form(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']

        widgets={
            'username':forms.TextInput(attrs={'class':'form-control',
                                              'placeholder': 'Enter your username . . .'}),
            'email':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder': 'Enter your email . . .'}),
            'password':forms.PasswordInput(attrs={'class':'form-control',
                                                  'placeholder': 'Enter password . . .'})
        }

class UserProfile_Form(forms.ModelForm):
    class Meta:
        model=UserProfile_Model
        fields=['name','age','height','weight','gender','profile_picture']
        read_only_fields=['user','created_date','updated_date','is_active']

        widgets={

            'name':forms.TextInput(attrs={'class':'form-control',
                                          'placeholder': 'Enter your name'}),
            'age':forms.NumberInput(attrs={'class':'form-control',
                                            'placeholder':'Enter Your age'}),
            'height':forms.NumberInput(attrs={'class':'form-control',
                                               'placeholder':'Enter Your height in cm'}),
            'weight':forms.NumberInput(attrs={'class':'form-control',
                                               'placeholder':'Enter your weight in Kg'}),
            'gender':forms.Select(attrs={'class':'form-control'}),

            'profile_picture':forms.FileInput(attrs={'class':'form-control-file',
                                                      'id':'profile_image'})   #id is given because it will be useful for JavaScript interactions or CSS.
        } 

class Login_Form(forms.Form):

    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control',
                                                                            'placeholder':'Username . . .'}))
    password=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control',
                                                                           'placeholder':'password . . .'}))
    
class BMRForm(forms.Form):
    choice = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    height = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your height in cm . . .'}))
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your weight in kg . . '}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age . . .'}))
    gender = forms.ChoiceField(choices=choice,widget=forms.Select(attrs={'class': 'form-control . . .'}))


class FoodForm(forms.ModelForm):

    class Meta:
        model=Foods
        fields="__all__"
        widgets={
                 'name':forms.TextInput(attrs={'class':'form-control',
                                          'placeholder': 'Foodname'}),
                 'calorie':forms.NumberInput(attrs={'class':'form-control',
                                            'placeholder':'Calorie'}),
        }

class Exercise_Form(forms.ModelForm):

    class Meta:

        model=Exercise
        fields="__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter exercise name'}),

            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),

            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter duration in minutes'}),

            'reps': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter count of reps'}),

            'calories_burned': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter  amount of calories burns'}),

            'gif': forms.FileInput(attrs={'class': 'form-control'}),
        }

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        label='End Date'
    )

class SleepForm(forms.Form):

    sleep_start_time=forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local',"class":"form-control"}))

    sleep_end_time=forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local',"class":"form-control"}))

    notes=forms.CharField(max_length=100,widget=forms.Textarea(attrs={"class":"form-control","rows":3}))

    
class UserFoodForm(forms.ModelForm):
    class Meta:
        model = UserFood
        fields = ['food', 'quantity']
        read_only_fields=['user','total_calories']
        widgets = {
            'food': forms.Select(attrs={'class': 'form-control'}),

            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter how much'}),
        }    

class Userfood_Daterange(forms.Form):
    start = forms.DateField(
        widget=forms.TextInput(attrs={'type':'date'}),
        label='start'
    )
    end = forms.DateField(
        widget=forms.TextInput(attrs={'type':'date'}),
        label='end'
    )

