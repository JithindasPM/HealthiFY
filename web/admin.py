from django.contrib import admin

# Register your models here.


from web.models import Foods
from web.models import Exercise
from web.models import Consultant

admin.site.register(Foods)
admin.site.register(Exercise)
admin.site.register(Consultant)


