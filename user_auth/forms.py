from django import forms
from helper import logger
import logging
class LoginForm(forms.Form):
    username=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Enter your Username'}))
    password=forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))
class StudentForm(forms.Form):
    first_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':"ألاسم الاول"}))
    middle_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':"ألاسم الاوسط"}))
    last_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':"ألاسم الاخر"}))
    guardian_phone=forms.CharField(max_length=10,min_length=10,required=True,widget=forms.TextInput(attrs={'placeholder':"رقم هاتف ولي الأمر"}))
    def clean(self):
        cleaned_data=super().clean()
        pn=cleaned_data['guardian_phone']
        log=logger('clean',logging.INFO,'add_student')
        log.error('is good for now')
        if not pn.isdigit():
            raise Exception('لا يمكن لرقم الهاتف ان يحتوي على احرف')
        if not  pn.startswith(('077','078','079')):
            raise Exception('رقم الهاتف غير صحيح')
        return cleaned_data
class UserForm(forms.Form):
    first_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':"ألاسم الاول",'class':'form-input'}))
    middle_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':"ألاسم الاوسط",'class':'form-input'}))
    last_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':"ألاسم الاخر",'class':'form-input'}))
    username=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':"اسم المستخدم",'class':'form-input'}))
    email=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder':"البريد الالكتروني",'class':'form-input'}))
    password=forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':"كلمة المرور",'class':'form-input'}))
    phone=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':"رقم الهاتف",'class':'form-input','maxlength':10,'minlength':10}))
   
    def clean(self):
        cleaned_data=super().clean()
        pn=cleaned_data['phone']
        log=logger('clean',logging.INFO,'add_student')
        log.error('is good for now')
        if not pn.isdigit():
            raise Exception('لا يمكن لرقم الهاتف ان يحتوي على احرف')
        if not  pn.startswith(('077','078','079')):
            raise Exception('رقم الهاتف غير صحيح')
        return cleaned_data