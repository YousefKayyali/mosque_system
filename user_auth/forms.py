from django import forms
class LoginForm(forms.Form):
    username=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Enter your Username'}))
    password=forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))