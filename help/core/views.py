from django.shortcuts import render

def HomeAction(request):
    return render(request, "core/home.html")
    