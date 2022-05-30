from django.shortcuts import render, HttpResponse

# Create your views here.
def indexPage(request):
    context = {
        'variable' : 'hello django!!!'
    }
    # return HttpResponse('This is indexPage ....')
    return render(request, 'index.html', context)

def about(request):
    return HttpResponse('This is about ....')

def services(request):
    return HttpResponse('This is services ....')