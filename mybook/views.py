from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):
    user = request.user
    hello = "hello World"
    context = {
        'user':user,
        'hello' : hello
    }
    return render(request, 'mybook/home.html', context)
    #return HttpResponse("Hello world")