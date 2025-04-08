from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
import backend.forms as forms
import backend.models as models
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

def register_user(request):  #reused from the past year's course project
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login'].replace('/','')
            try:  # check for existing users
                user = User.objects.get(username=user_login)
                return render(request, 'backend/register.html', {'form': form,'register':False, 'user_found': True})
            except:
                pass  # no existing user found, proceed
            user_password = form.cleaned_data['password']
            if user_password != form.cleaned_data['password_verify']:  # passwords did not match
                return render(request, 'backend/register.html', {'form': form,'register':False, 'password_mismatch': True})
            user_email = form.cleaned_data['email']

            if (not user_login) or (not user_email) or (not user_password):  # in the case of whether some credentials have been skipped
                return render(request, 'backend/register.html', {'form': form,'register':False, 'incomplete_form': True})

            user = User.objects.create_user(user_login, user_email, user_password)
            user.save()  # created the user
            if user is not None:  # login the newly created user
                print('New User Logging in '+user_login)  # for the tests
                login(request, user)
                #create the permissions object
                perm_obj=models.UserPerms(user=user)
                #temporary measure
                perm_obj.is_teacher=True
                perm_obj.save()
            return HttpResponseRedirect('/')
    else:  # prompt the form
        form = forms.RegisterForm()
        if request.user.is_authenticated:  # if logged in, redirect to the main page
            return HttpResponseRedirect('/')
    return render(request, 'backend/register.html', {'form': form,'register':False})

def login_user(request):
    forward_path=request.GET.get('next','/')
    print(forward_path)
    if request.method == 'POST':  # look for the imports
        form = forms.AuthForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user = authenticate(username=user_login, password=user_password)

            if request.user.is_authenticated:  # if logged in, redirect to the main page
                return HttpResponseRedirect(forward_path)

            if user is not None:  # accept the form and login the user
                print('Logging in '+user_login)  # for the tests
                login(request, user)
                return HttpResponseRedirect(forward_path)
            else:  # failed credentials check
                form = forms.AuthForm()
                return render(request, 'backend/login.html', {'form': form,'register':False, 'failed_login': True,'next':forward_path})
    else:  # prompt the form
        form = forms.AuthForm()
        if request.user.is_authenticated:  # if logged in, redirect to the main page
            return HttpResponseRedirect(forward_path)
    return render(request, 'backend/login.html', {'form': form,'register':False,'next':forward_path})

def logout_user(request):
    if request.user.is_authenticated:
        print('Logging out '+request.user.username)
        logout(request)
    return HttpResponseRedirect('/login/')

@login_required
def home(request):
    return render(request,'backend/home.html',{'user':request.user})

@login_required
def profile_page(request):
    return render(request,'backend/profile_page.html',{'user':request.user})

@login_required
def profile_page_edit(request):
    user_obj=request.user
    #retrieve the additional info object
    try:
        info_obj=models.UserInfo.objects.filter(user=request.user)[0]
    except IndexError:
        info_obj=models.UserInfo(user=request.user)
    
    if request.method=="POST":
        form=forms.UserEditForm(request.POST,request.FILES)
        if form.is_valid():
            if request.FILES:
                #remove the old pfp
                info_obj.pfp.delete(save=True)
            try:
                info_obj.pfp=form.cleaned_data['pfp']
                extension=info_obj.pfp.name.split('.')[-1]
                #print(extension)
                info_obj.pfp.name=request.user.username+'.'+extension
                info_obj.save()
            except AttributeError:
                pass
            
            #deal with the rest of the form
            new_username=form.cleaned_data['username'].replace('/','').replace('?','')
            print('input',new_username)
            if new_username:
                #check if the username is already taken
                try:
                    lookup=User.objects.filter(username=new_username)[0]
                    return HttpResponseRedirect('/profile/edit/?username_taken=true')
                except IndexError:
                    pass
                user_obj.username=new_username
            old_password=form.cleaned_data['old_password']
            new_password=form.cleaned_data['password']
            verify_password=form.cleaned_data['password_verify']
            if old_password and new_password and verify_password:
                upd_user=authenticate(request,username=request.user,password=old_password)
                print(upd_user)
                if upd_user is None: #credentials didn't match
                    return HttpResponseRedirect('/profile/edit/?wrong_password=true')
                if new_password==verify_password:
                    user_obj.set_password(new_password)
                else:
                    return HttpResponseRedirect('/profile/edit/?password_mismatch=true')

            user_obj.save()
            
            return HttpResponseRedirect('/profile/edit/?success=true')
        return HttpResponseRedirect('/profile/edit/')
                
    #GET
    form=forms.UserEditForm()               
    
    return render(request,'backend/profile_page_edit.html',{'user':request.user,'form':form})