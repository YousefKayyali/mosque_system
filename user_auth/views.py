from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from .forms import LoginForm
import logging
logging.basicConfig(level=10)
def login_user(request):
    if request.method=="POST":
        lf=LoginForm(request.POST,request.FILES)
        if lf.is_valid():
            password=lf.cleaned_data['password']
            username=lf.cleaned_data['username']
            user=authenticate(username=username,password=password)
            if user :
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'incorrect username or password')
                return redirect('login')  
    else:
        lf=LoginForm()
    context={'form':lf}
    return render(request,r'user_auth\login.html',context=context)
def logout_user(request):
    logout(request)
    return redirect('login')