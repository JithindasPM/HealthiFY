from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save


class UserProfile_Model(models.Model):

    name=models.CharField(max_length=100,null=True)

    age=models.PositiveIntegerField(null=True)

    height=models.IntegerField(null=True)

    weight=models.IntegerField(null=True)

    gender=models.CharField(max_length=100,choices=[('male','male'),
                                                    ('female','female')],null=True)
    
    profile_picture=models.FileField(upload_to='images',null=True,blank=True)

    user=models.OneToOneField(User,on_delete=models.CASCADE)

    created_date=models.DateField(auto_now_add=True)  

    updated_date=models.DateField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name


    def create_profile(sender,instance,created,**kwargs):
        if created:      
            UserProfile_Model.objects.update_or_create(user=instance)
    post_save.connect(sender=User,receiver=create_profile)



class Foods(models.Model):

    name=models.CharField(max_length=50,db_index=True,unique=True)
    calorie=models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class my_model(models.Model):
    name=models.CharField(max_length=100)


