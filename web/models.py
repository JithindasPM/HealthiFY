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
    

class Exercise(models.Model):

    name=models.CharField(max_length=200)   #name of the exercise

    description=models.TextField(blank=True,null=True)   #description of the exercise

    duration=models.CharField(max_length=100,default='60:00',blank=True,null=True)  # Duration of the exercise 

    reps=models.PositiveIntegerField(default=25,blank=True,null=True)   # Default number of repetitions set to 15

    calories_burned=models.PositiveIntegerField()  # Calories burned during the exercise

    gif=models.ImageField(upload_to="images/",blank=True,null=True)  # GIF of the exercise

    def __str__(self):
        return self.name


class Exercise_Data(models.Model):

    exercise=models.ForeignKey(Exercise,on_delete=models.CASCADE)   #exercise is connected with Exercise table

    user=models.ForeignKey(User,on_delete=models.CASCADE)    #user is conneted with User table

    created_date=models.DateField(auto_now_add=True,null=True)

    updated_date=models.DateField(auto_now_add=True,null=True)


    def __str__(self):
        return self.exercise,self.user
    

class SleepModel(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sleep_records")

    date=models.DateField(auto_now_add=True)

    sleep_start_time=models.DateTimeField()

    sleep_end_time=models.DateTimeField()

    notes=models.TextField(blank=True,null=True)


    def total_sleep_duration(self):
        return self.sleep_end_time - self.sleep_start_time
    
    def __str__(self):
        return f'{self.user.username} - {self.date}'


class UserFood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Foods, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_calories = models.PositiveIntegerField()
    created_date=models.DateField(auto_now_add=True,null=True)
    upated_date=models.DateField(auto_now=True,null=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}"
    

class Consultant(models.Model):

    name=models.CharField(max_length=100,null=True)

    profile_picture=models.FileField(upload_to='images',null=True,blank=True)

    specialization=models.CharField(max_length=100,null=True)

    experience=models.IntegerField(null=True)

    certifications=models.CharField(max_length=100,null=True)

    location=models.CharField(max_length=100,null=True)

    job=models.CharField(max_length=100,choices=[('trainer','trainer'),
                                                    ('nutritionist','nutritionist')],null=True)

    created_date=models.DateField(auto_now_add=True)  

    updated_date=models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
class Food_Goal(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.PositiveIntegerField(null=True)
    created_date=models.DateField(auto_now_add=True) 

    class Meta:
        unique_together = ('user', 'created_date') 

class Exercise_Goal(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_calories = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}"

class Exercise_Goal_Model(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    goal=models.PositiveIntegerField(null=True)
    created_date=models.DateField(auto_now_add=True) 

    class Meta:
        unique_together = ('user', 'created_date') 
    
    def __str__(self):
        return f"{self.goal}"
    

class Community(models.Model):
    name = models.CharField(max_length=255)
    description=models.TextField(null=True,blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_community')
    members = models.ManyToManyField(User, related_name='communities')
    created_date=models.DateField(auto_now_add=True)  
    updated_date=models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
class Chat(models.Model):
    community = models.ForeignKey('Community', on_delete=models.CASCADE, related_name='messages') 
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages') 
    message = models.TextField() 
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.sender.username}: {self.message[:30]}..." 