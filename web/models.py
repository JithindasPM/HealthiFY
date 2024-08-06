from django.db import models

from django.contrib.auth.models import User


class UserProfile_Model(models.Model):

    name=models.CharField(max_length=100)

    age=models.PositiveIntegerField()

    height=models.IntegerField()

    weight=models.IntegerField()

    gender=models.CharField(max_length=100,choices=[('male','male'),
                                                    ('female','female')])
    
    profile_picture=models.ImageField(upload_to='images')

    created_date=models.DateField(auto_now_add=True)

    updated_date=models.DateField(auto_now=True)

    is_active=models.BooleanField(default=True)
