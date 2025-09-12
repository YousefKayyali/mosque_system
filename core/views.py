from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import StudentForm,MemorizationForm
from django.contrib import messages
from user_auth.models import Students,Profiles,Users    
from .models import QuranMemorization
import logging
from helper import logger
from django.utils.timezone import now

@login_required
def home(requests):
    return render(requests,r'home.html')
@login_required
def add_student(request):
    context={'title':'أضافة طالب'}
    if request.method=='POST':
        sf=StudentForm(request.POST,request.FILES)
        try:
            if sf.is_valid():
                p=Profiles(first_name=sf.cleaned_data['first_name'],middle_name=sf.cleaned_data['middle_name'],last_name=sf.cleaned_data['last_name'],created_date=now(),is_active=True)
                p.save()
                s=Students(profile_id=p.profile_id,guardian_phone=sf.cleaned_data['guardian_phone'],date_of_birth=request.POST.get('date_of_birth'))
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
def add_memorization(request):
    context={'title':'تسجيل التسميع'}
    st=Students.objects.all()
    log=logger('check data ',logging.INFO,'add memorization')
    log.info(st[0].student_id)

    context['students']=st
    if request.method=='POST':
        mf=MemorizationForm(request.POST,request.FILES)
        if mf.is_valid():
           temp=False
           st_id=request.POST.get('student')
           user_id=request.user.user_id
           evaluation=request.POST.get('evaluation')
           memorization_type=request.POST.get('memorization_type')
           if '' in (st_id,user_id,evaluation,memorization_type):
               temp=True
               messages.error(request,'مدخل غير صحيح يرجى أعادة المحاولة')
               return redirect('add_memorization')
           q=QuranMemorization(student=Students.objects.get(student_id=st_id),user=Users.objects.get(user_id=user_id),from_page=mf.cleaned_data['from_page'],to_page=mf.cleaned_data['to_page'],from_verse=mf.cleaned_data['from_verse'],to_verse=mf.cleaned_data['to_verse'],evaluation=evaluation,number_of_misses=mf.cleaned_data['number_of_misses'],note=mf.cleaned_data['note'],record_date=now(),memorization_type=memorization_type)
           q.save()
           messages.success(request,'تم تسجيل التسميع')
           return redirect('add_memorization')
        else:
           log.info(mf.errors)

        
    mf=MemorizationForm()
    context['form']=mf
    return render(request,r'add_memorization.html',context)
