from django.shortcuts import render
from .models import Profile
# Create your views here.

def my_profile_view(request):
    obj = Profile.objects.get(user=request.user)
    user_context = {
        'user_object' : obj
    }
    return render(request, 'profiles/profile.html', user_context)