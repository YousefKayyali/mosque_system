from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm,StudentForm,UserForm
import logging
from helper import logger
from .models import Profiles,Users,Students,ProfilesPrivilege,Privileges
from django.utils.timezone import now
from django.db import transaction

logging.basicConfig(level=10)
def login_user(request):
    if request.method=="POST":
        lf=LoginForm(request.POST,request.FILES)
        if lf.is_valid():
            password=lf.cleaned_data['password']
            username=lf.cleaned_data['username']
            user=authenticate(username=username,password=password)
            if user :
                privilege=ProfilesPrivilege.objects.filter(profile_id=user.profile).values_list('privilege_id',flat=True)
                login(request,user)
                request.session['privileges']=list(privilege)

                return redirect('home')
            else:
                messages.error(request,'incorrect username or password')
                return redirect('login')  
    else:
        lf=LoginForm()
    context={'form':lf}
    return render(request,r'login.html',context=context)
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def add_student(request):
    context={'title':'أضافة طالب'}
    if request.method=='POST':
        sf=StudentForm(request.POST,request.FILES)
        try:
            if sf.is_valid():
                p=Profiles(first_name=sf.cleaned_data['first_name'],middle_name=sf.cleaned_data['middle_name'],last_name=sf.cleaned_data['last_name'],created_date=now(),is_active=True)
                p.save()
                s=Students(profile_id=p.profile_id,guardian_phone=sf.cleaned_data['guardian_phone'],date_of_birth=request.POST.get('date_of_birth'),points=0)
                s.save()
                messages.success(request,'تم اضافة الطالب')
                return redirect('add_student')
            else:
                log=logger('form error ',logging.DEBUG,'add_student')
                log.error(f'{sf.errors}')
                messages.error(request,'لم يتم أضافة الطالب هناك خطاء')
                return redirect('add_student')
        except Exception as e:
            messages.error(request,str(e))
            return redirect('add_student')
    sf=StudentForm()
    context['form']=sf
    return render(request,r'add_student.html',context)
@login_required
def add_user(request):
    context={'title':'أضافة مشرف'}
    log=logger('add_user',logging.INFO,'add_user')
    if request.method=="POST":
        uf=UserForm(request.POST,request.FILES)
        if uf.is_valid():
                try:
                    with transaction.atomic():
                        p=Profiles(first_name=uf.cleaned_data['first_name'],middle_name=uf.cleaned_data['middle_name'],last_name=uf.cleaned_data['last_name'],created_date=now(),is_active=True)
                        p.save()
                        u=Users(profile=p,username=uf.cleaned_data['username'],email=uf.cleaned_data['email'],password=uf.cleaned_data['password'],phone=uf.cleaned_data['phone'] )
                        u.save()
                        pp=ProfilesPrivilege(profile=p,privilege=Privileges.objects.get(privilege_id=request.POST.get('privilege',None)))
                        pp.save()
                        messages.success(request,'تم أضافة المشرف')
                        return redirect('add_user')
                except Exception as e:
                    messages.error(request,str(e))
                    return redirect('add_user')
        else:   
            log.error(uf.errors)
            messages.error(request,'لم يتم أضافة المشرف هناك خطاء')
            return redirect('add_user')
            
    uf=UserForm()
    context['form']=uf
    return render(request,'add_user.html',context)