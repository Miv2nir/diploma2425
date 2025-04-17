from django import forms
from backend import models

#TODO: refactor for some fancy new css that doesn't suck
#essentials
class RegisterForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'login-input-box','id':'email_field'}))
    login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'placeholder': 'Login','class': 'login-input-box','id':'login_field'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'login-input-box','id':'password_field'}))
    password_verify = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password','class': 'login-input-box','id':'verification_field'})) #, 'class': 'square_login' - cut out as no css work is done at this point

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class AuthForm(forms.Form):
    # login = forms.CharField(label='Login', max_length=100)
    login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'placeholder': 'Login', 'class': 'login-input-box','id':'login_field'}))

    # password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'login-input-box','id':'password_field'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
            
#main page forms n whatnot

class UserEditForm(forms.Form):
    pfp=forms.ImageField(required=False,widget=forms.FileInput(attrs={'onchange':'updateLabel();'}))
    delete_pfp=forms.BooleanField(required=False)
    display_name = forms.CharField(label='Display Name',required=False,widget=forms.TextInput(attrs={'placeholder': 'Display Name','class': 'login-input-box'}))
    email = forms.CharField(label='Email',required=False, widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'login-input-box'}))
    login = forms.CharField(label='Login',required=False, widget=forms.TextInput(attrs={'placeholder': 'Login','class': 'login-input-box'}))
    old_password = forms.CharField(required=False,label='Old Password', widget=forms.PasswordInput(attrs={'placeholder': 'Old Password','class': 'login-input-box'}))
    password = forms.CharField(required=False,label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'New Password','class': 'login-input-box'}))
    password_verify = forms.CharField(required=False,label='Repeat Password', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat New Password','class': 'login-input-box'}))

class SearchForm(forms.Form):
    search = forms.CharField(label='Search',required=False, widget=forms.TextInput(attrs={'placeholder': 'Type the project name here', 'class': 'search-box'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
            
class ProfileMetadataForm(forms.Form):
    icon=forms.ImageField(required=False,widget=forms.FileInput(attrs={'onchange':'updateLabel();'}))
    delete_icon=forms.BooleanField(required=False)
    name = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Project Name','class': 'login-input-box'}))
    description=forms.CharField(label='Description',required=False,widget=forms.Textarea(attrs={'placeholder':'Description','class':'login-input-box'}))
    
class DataFileForm(forms.ModelForm):
    class Meta:
        model= models.DataFile
        fields=['file','name','description']
        widgets = {
            'file':forms.FileInput(attrs={'onchange':'updateLabel();'})
        }