from django.contrib import admin
from AttendifyEvents .models import category,Event,CustomUser,sub_category

# Register your models here.

admin.site.register(category)
admin.site.register(sub_category)
admin.site.register(Event)
# admin.site.register(CustomUser)




