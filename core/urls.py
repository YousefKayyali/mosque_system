from django.urls import path,include
from .views import home ,add_student,add_memorization
urlpatterns = [
    path('',home,name='home'),
    path('add_student/',add_student,name='add_student'),
    path('add_memorization/',add_memorization,name='add_memorization'),
]
