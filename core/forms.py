from django import forms
import logging
from helper import logger
from .models import QuranMemorization
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
class MemorizationForm(forms.ModelForm):
    
    class Meta:
        model=QuranMemorization
        exclude=['record_date','user','student']
        widgets={
            'from_page':forms.NumberInput(attrs={'placeholder':'من الصفحة','min':1 ,'max':604}),
            'to_page':forms.NumberInput(attrs={'placeholder':'الى الصفحة','min':1 ,'max':604}),
            'from_verse':forms.NumberInput(attrs={'placeholder':'من الأية','min':1,'max':286}),
            'to_verse':forms.NumberInput(attrs={'placeholder':'الى الأية','class':'lelement','min':1,'max':286}),
            'number_of_misses':forms.NumberInput(attrs={'placeholder':'عدد الاخطاء','class':'relement','min':0 ,'max':3}),
            'note':forms.Textarea(attrs={'placeholder':'ملاحظات'})
        }
    def clean(self):
        clean=super().clean()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['note'].required=False

