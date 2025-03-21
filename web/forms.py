from django import forms

from web.models import User
from web.models import UserProfile_Model
from web.models import Foods
from web.models import Exercise
from web.models import UserFood
from web.models import Consultant
from web.models import Food_Goal
from web.models import Exercise_Goal_Model
from web.models import Community
from web.models import Chat
from web.models import Community

from django_select2.forms import Select2MultipleWidget


class Registration_Form(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']

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

            'name':forms.TextInput(attrs={'class':'form-control my-1',
                                          'placeholder': 'Enter your name . . .',
                                          'style':'background-color:rgba(255, 255, 255, 0.4)'}),
            'age':forms.NumberInput(attrs={'class':'form-control my-1',
                                            'placeholder':'Enter Your age . . .',
                                            'style':'background-color:rgba(255, 255, 255, 0.4)'}),
            'height':forms.NumberInput(attrs={'class':'form-control my-1',
                                               'placeholder':'Enter Your height in cm . . .',
                                               'style':'background-color:rgba(255, 255, 255, 0.4)'}),
            'weight':forms.NumberInput(attrs={'class':'form-control my-1',
                                               'placeholder':'Enter your weight in Kg . . .',
                                               'style':'background-color:rgba(255, 255, 255, 0.4)'}),
            'gender':forms.Select(attrs={'class':'form-control my-1',
                                         'style':'background-color:rgba(255, 255, 255, 0.4)'}),

            'profile_picture':forms.FileInput(attrs={'class':'form-control-file',
                                                      'id':'profile_image'})   #id is given because it will be useful for JavaScript interactions or CSS.
        } 


class Login_Form(forms.Form):

    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control my-1',
            'placeholder': 'Username . . .',
            'style': 'background-color:rgba(255, 255, 255, 0.4)'
        })
    )

    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control my-1',
            'placeholder': 'Password . . .',
            'style': 'background-color:rgba(0, 0, 0, 0.7)'
        })
    )
    
class BMRForm(forms.Form):
    choice = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    height = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control my-1',
                                                             'placeholder': 'Enter your height in cm . . .',
                                                             'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}))
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control my-1',
                                                               'placeholder': 'Enter your weight in kg . . ',
                                                               'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control my-1',
                                                              'placeholder': 'Enter your age . . .',
                                                              'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}))
    gender = forms.ChoiceField(choices=choice,widget=forms.Select(attrs={'class': 'form-control my-1',
                                                                        'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}))


class FoodForm(forms.ModelForm):

    class Meta:
        model=Foods
        fields="__all__"
        widgets={
                 'name':forms.TextInput(attrs={'class':'form-control my-1',
                                          'placeholder': 'Foodname . . .','style':'background-color:rgba(255, 255, 255, 0.5)'}),
                 'calorie':forms.NumberInput(attrs={'class':'form-control my-1',
                                            'placeholder':'Calorie . . .','style':'background-color:rgba(255, 255, 255, 0.5)'}),
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

    notes=forms.CharField(max_length=100,widget=forms.Textarea(attrs={"class":"form-control","rows":3,"style": "background-color: rgba(255, 255, 255, 0.45);color: black;"}))

    
class UserFoodForm(forms.ModelForm):
    class Meta:
        model = UserFood
        fields = ['food', 'quantity']
        read_only_fields=['user','total_calories']
        widgets = {
            'food': forms.Select(attrs={'class': 'form-control my-1'}),

            'quantity': forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'Enter how much . . .'}),
        }  


class Userfood_Daterange(forms.Form):
    start = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control shadow-sm',
                'placeholder': 'Select start date',
                'style': 'border-radius: 10px;'
            }
        ),
        label='From',
        label_suffix='',  # Removes the colon after label
    )
    
    end = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control shadow-sm',
                'placeholder': 'Select end date',
                'style': 'border-radius: 10px;'
            }
        ),
        label='To',
        label_suffix='',
    )


class Consultant_Form(forms.ModelForm):
    class Meta:
        model=Consultant
        fields=['name','profile_picture','specialization','experience','certifications','location','job']
        read_only_fields=['created_date','updated_date']

        widgets={

            'name':forms.TextInput(attrs={'class':'form-control my-1',
                                          'placeholder': 'Enter your name . . .',
                                          'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}),
            'profile_picture':forms.FileInput(attrs={'class':'form-control-file',
                                                      'id':'profile_image'}),
            'specialization':forms.TextInput(attrs={'class':'form-control my-1',
                                          'placeholder': 'Enter your name . . .',
                                          'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}),
            'experience':forms.NumberInput(attrs={'class':'form-control my-1',
                                            'placeholder':'Enter Your age . . .',
                                            'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}),
            'certifications':forms.TextInput(attrs={'class':'form-control my-1',
                                          'placeholder': 'Enter your name . . .',
                                          'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}),
            'location':forms.TextInput(attrs={'class':'form-control my-1',
                                          'placeholder': 'Enter your name . . .',
                                          'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}),
            'job':forms.Select(attrs={'class':'form-control my-1',
                                         'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}),

            
        } 

class Food_Goal_Form(forms.ModelForm):
    class Meta:
        model = Food_Goal
        fields = ['goal']
        read_only_fields=['user','created_date']
        widgets = {

            'goal':forms.NumberInput(attrs={'class':'form-control my-1',
                                            'placeholder':'Enter your goal in calories . . .',
                                            'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'})
        }   

class Exercise_Goal_Form(forms.ModelForm):
    class Meta:
        model=Exercise_Goal_Model
        fields=['goal']
        read_only_fields=['user','created_date']
        widgets = {

            'goal':forms.NumberInput(attrs={'class':'form-control my-1',
                                            'placeholder':'Enter your goal in calories . . .',
                                            'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'})
        }  


class Community_Form(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'members','description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control my-1',
                'placeholder': 'Community name . . .',
                'style': 'background-color:rgba(0, 0, 0, .95); border:2px solid rgba(0, 0, 0, 0.1)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description...',
                'rows': 3,  # Adjust number of visible rows
                'style': 'resize: none; height: 80px;'  # Prevent resizing and set a fixed height
            }),
            'members': Select2MultipleWidget(attrs={'class': 'form-control'})  # Use Select2MultipleWidget
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['members'].queryset = User.objects.exclude(id=user.id)

class Chat_Form(forms.ModelForm):
    class Meta:
        model=Chat
        fields=['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Type your message...',
                'rows': 3
            }),
        }
    
class Groq_Chat_Form(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control my-1',
            'placeholder': 'Ask anything . . .',
            'style': 'background-color:rgba(255, 255, 255, 0.4); height: 100px;',  # Adjust height
            'rows': 3,  # Set initial rows
        })
    )