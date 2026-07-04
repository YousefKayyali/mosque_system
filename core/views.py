from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import StudentForm,MemorizationForm
from django.contrib import messages
from user_auth.models import Students,Profiles,Users,Absences   
from .models import QuranMemorization,Points
import logging
from helper import logger
from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import psycopg2 
import json
@login_required
def home(requests):
    return render(requests,r'home.html')

@login_required
def add_memorization(request):
    # if Absences.objects.filter(day_date=now().date()).exists():
    #     absencse='disabled'
    # else:
    #     absencse=''
        
    context={'title':'تسجيل التسميع'}
    # context['absencse_form']=absencse
    query='''
WITH abs AS (
    SELECT student_id, COUNT(DISTINCT day_date) AS absences
    FROM absences
    GROUP BY student_id
),
pts AS (
    SELECT student_id, SUM(point) AS total_points
    FROM points
    GROUP BY student_id
),
mem AS (
    SELECT student_id,
           SUM(
                pages
           ) AS total_diff
    FROM quran_memorization
	where evaluation !='did not memorize'
    GROUP BY student_id
)
SELECT s.student_id,
       p.first_name, p.middle_name, p.last_name,
       COALESCE(mem.total_diff,0) AS total_diff,
       COALESCE(abs.absences,0) AS total_absences,
       COALESCE(pts.total_points,0) AS total_points,
	   rank()over(    ORDER BY COALESCE(mem.total_diff,0) DESC,
            						 COALESCE(pts.total_points,0) DESC,
             						COALESCE(abs.absences,0)) as rank
FROM students s
JOIN profiles p USING(profile_id)
LEFT JOIN abs USING(student_id)
LEFT JOIN pts USING(student_id)
LEFT JOIN mem USING(student_id)
 where s.student_id !=1
order by total_diff desc ,total_points desc ,total_absences;
            '''
    with psycopg2.connect(host='localhost',database='mosque_system',port=5432,password='postgres',user='postgres') as conn:
        with conn.cursor() as cursor:
            cursor.execute(query=query)
            st=cursor.fetchall()
    log=logger('check data ',logging.INFO,'add memorization')
    context['students']=st
    log.info(now().date())
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

            evaluation_point={
                'excellent':2,
                'very good':1,
                'good':0,
                'did not memorize':0,
            }
            points=0
            if  not request.POST.get('manual_points',None):

                points=evaluation_point[evaluation] - min(request.POST.get('number_of _try',0),2)
                log.info(points)
                if  points !=0:
                    pages=mf.cleaned_data['pages']
                    if pages!=0:
                        points*=pages

            else:
                points=request.POST.get('manual_points',None)
            q=QuranMemorization(student=Students.objects.get(student_id=st_id),user=Users.objects.get(user_id=user_id),from_page=mf.cleaned_data['from_page'],pages=mf.cleaned_data['pages'],evaluation=evaluation,number_of_misses=mf.cleaned_data['number_of_misses'],note=mf.cleaned_data['note'],record_date=now(),memorization_type=memorization_type)
            q.save()
            p=Points(student=q.student,point=points,note=None,date_of_insert=q.record_date)
            p.save()
            log.info(
                f"{request.session.get('student_name', mf.cleaned_data.get('student'))} | "
                f"from_page={mf.cleaned_data.get('from_page')} | "
                f"pages={mf.cleaned_data.get('pages')} | "
                f"evaluation={mf.cleaned_data.get('evaluation')} | "
                f"misses={mf.cleaned_data.get('number_of_misses')} | "
                f"note={mf.cleaned_data.get('note')} | "
                f"date={mf.cleaned_data.get('record_date')} | "
                f"type={mf.cleaned_data.get('memorization_type')}"
            )
            messages.success(request,'تم تسجيل التسميع')
            return redirect('add_memorization')
        elif request.POST.get('absense',None):
            log.info(request.POST.getlist('absense',None))
            try:
                with psycopg2.connect(host='localhost',database='mosque_system',port=5432,password='postgres',user='postgres') as conn:
                    with conn.cursor() as cursor:
                        query='''
                                INSERT INTO absences(student_id)
                                values(%s)
                            '''
                        cursor.executemany(query,[(i,) for i in request.POST.getlist('absense')])
                        conn.commit() 
            except Exception as e:
                log.error(str(e))
                messages.error(request,'لم يتم تسجيل الحضور و الغياب أعد المحاوله')
            finally:
                return redirect('add_memorization')

        else:
            for i in st:
                if request.POST.get(f'add_point_{i[0]}',None):
                    p=Points(student=Students.objects.get(student_id=i[0]),point=request.POST.get(f'add_point_{i[0]}'),note=request.POST.get(f'add_point_note_{i[0]}'),date_of_insert=now().date())
                    p.save()
                    break
            return redirect('add_memorization')


    mf=MemorizationForm()
    context['form']=mf
    return render(request,r'add_memorization.html',context)
def review_memorization(request):
    # استرجاع كل الطلاب مع بياناتهم الشخصية
    students = Students.objects.select_related("profile").values(
        "student_id",
        "profile__first_name",
        "profile__middle_name",
        "profile__last_name"
    )
    return render(request, 'review_memorization.html', {"students": students})

def get_records(request, student_id):
    # جلب جميع سجلات التسميع للطالب
    records = list(QuranMemorization.objects.filter(student_id=student_id).values(
        "memorization_id",
        "record_date",
        "memorization_type",
        "from_page",
        "pages",
        "evaluation",
        "number_of_misses",
        "note"
    ))
    return JsonResponse({"success": True, "data": records})

@csrf_exempt
def update_record(request, record_id):
    if request.method == "POST":
        data = json.loads(request.body)
        QuranMemorization.objects.filter(memorization_id=record_id).update(
            memorization_type=data.get("memorization_type"),
            from_page=data.get("from_page"),
            pages=data.get("pages"),
            evaluation=data.get("evaluation"),
            number_of_misses=data.get("number_of_misses"),
            note=data.get("note"),
        )
        return JsonResponse({"success": True, "message": "تم التعديل بنجاح"})
    return JsonResponse({"success": False, "message": "خطأ في الطلب"})

@csrf_exempt
def delete_record(request, record_id):
    QuranMemorization.objects.filter(memorization_id=record_id).delete()
    return JsonResponse({"success": True, "message": "تم حذف السجل"})