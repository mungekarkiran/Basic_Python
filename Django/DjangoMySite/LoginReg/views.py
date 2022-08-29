from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import NewUsers

# Create your views here.
def loginReg(request):
    # return HttpResponse('<h1>hello</h1>')
    return render(request, 'index.htm')
    
def register(request):
    if request.method=='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        gender = request.POST.get('gender')
        if pwd1==pwd2:
            user = NewUsers(fname=fname,lname=lname,email=email,pwd1=pwd1,gender=gender)
            user.save()
            print('data inserted in table!!')
        else:
            print('pwd not match!!')    
        return redirect('/')
    else:
        return render(request, 'index.htm')
    
def login(request):
    return render(request, 'login.htm')