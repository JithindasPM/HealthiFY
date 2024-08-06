from django import forms

from web.models import User
from web.models import UserProfile_Model

class Registration_Form(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']

        widgets={
            'username':forms.TextInput(attrs={'class':'form-control',
                                              'placeholder': 'Enter your username'}),
            'email':forms.TextInput(attrs={'class':'form-control',
                                              'placeholder': 'Enter your email'}),
            'password':forms.PasswordInput(attrs={'class':'form-control',
                                              'placeholder': 'Enter password'})
        }

class UserProfile_Model_Form(forms.ModelForm):
    class Meta:
        model=UserProfile_Model
        fields="__all__"
        read_only_field=['user','created_date','updated_date','is_active']

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control',
                                              'placeholder': 'Enter your name'})
        }