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
                                          'placeholder': 'Enter your name'}),
            'age':forms.NumberInput(attrs={'class':'form-control',
                                            'placeholder':'Enter Your age'}),
            'height':forms.NumberInput(attrs={'class':'form-control',
                                               'placeholder':'Enter Your height in cm'}),
            'weight':forms.NumberInput(attrs={'class':'form-control',
                                               'placeholder':'Enter your weight in Kg'}),
            'gender':forms.RadioSelect(attrs={'class':'form-control'}),

            'profile_picture':forms.FileInput(attrs={'class':'form-control-file',
                                                      'id':'profile_image'})   #id is given because it will be useful for JavaScript interactions or CSS.
        } 