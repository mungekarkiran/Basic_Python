from django.shortcuts import render, HttpResponse

# Create your views here.
def indexPage(request):
    return HttpResponse('This is indexPage ....')

def about(request):
    return HttpResponse('This is about ....')

def services(request):
    return HttpResponse('This is services ....')