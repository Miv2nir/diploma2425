from django import forms
from backend import models

#TODO: refactor for some fancy new css that doesn't suck
#essentials
class RegisterForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'login-input-box'}))
    login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'placeholder': 'Login','class': 'login-input-box'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'login-input-box'}))
    password_verify = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password','class': 'login-input-box'})) #, 'class': 'square_login' - cut out as no css work is done at this point

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class AuthForm(forms.Form):
    # login = forms.CharField(label='Login', max_length=100)
    login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'placeholder': 'Login', 'class': 'login-input-box'}))

    # password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'login-input-box'}))
