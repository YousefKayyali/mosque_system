from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('add_memorization/',views.add_memorization,name='add_memorization'),
        path('review_memorization/', views.review_memorization, name='review_memorization'),

    path('get_records/<int:student_id>/', views.get_records, name='get_records'),
    path('update_record/<int:record_id>/', views.update_record, name='update_record'),
    path('delete_record/<int:record_id>/', views.delete_record, name='delete_record'),
]

