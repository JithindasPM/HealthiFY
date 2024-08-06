from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save



class UserProfile_model(models.Model):

    name=models.CharField(max_length=100)

    age=models.PositiveIntegerField()

    height=models.IntegerField()

    weight=models.IntegerField()

    gender=models.CharField(max_length=100,choices=[('male','male'),
                                                    ('female','female')])
    
    profile_picture=models.ImageField(upload_to='images')

    user=models.OneToOneField(User,on_delete=models.CASCADE)

    created_date=models.DateField(auto_now_add=True)

    updated_date=models.DateField(auto_now=True)

    is_active=models.BooleanField(default=True)


def create_profile(sender,instance,created,**kwargs):

    if created:

        UserProfile_model.objects.create(user=instance)

post_save.connect(sender=User,receiver=create_profile)
