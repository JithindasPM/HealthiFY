from django import forms

from web.models import User
from web.models import UserProfile_Model
from web.models import Foods

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
        