from django.shortcuts import render
from django.contrib.auth import authenticate, login


def home(request):
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(request, username=username, password=password)
    # if user is not None:
    #     login(request, user)

    context = {}
    return render(request, 'home.html', context=context)
