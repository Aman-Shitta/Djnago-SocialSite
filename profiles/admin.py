from django.contrib import admin
from .models import Profile, Relationship   # to register Profile to admin-panel 
# Register your models here.

admin.site.register(Profile)
admin.site.register(Relationship)