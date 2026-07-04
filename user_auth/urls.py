    
from django.contrib import admin
from django.urls import path,include
from user_auth.views import login_user,logout_user
from .views import add_student,add_user
urlpatterns = [
path('add_student/',add_student,name='add_student'),
path('add_user/', add_user,name='add_user')
]