from django.shortcuts import render

# Create your views here.
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
import backend.forms as forms
import backend.models as models
from backend.functions import *
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
                #create the additional info object
                info_obj=models.UserInfo(user=user,display_name=user.username)
                info_obj.save()
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
    #retrieve pfp
    try:
        pfp_obj=models.UserPFP.objects.filter(user=request.user)[0]
    except IndexError:
        pfp_obj=models.UserPFP(user=request.user)
    
    if request.method=="POST":
        form=forms.UserEditForm(request.POST,request.FILES)
        if form.is_valid():
            print(request.FILES)
            if request.FILES.get('pfp', False) or form.cleaned_data['delete_pfp']:
                print('removing pfp')
                #remove the old pfp
                pfp_obj.pfp.delete(save=True)
            try:
                pfp_obj.pfp=form.cleaned_data['pfp']
                extension=pfp_obj.pfp.name.split('.')[-1]
                #print(extension)
                pfp_obj.pfp.name=request.user.username+'.'+extension
                pfp_obj.save()
            except AttributeError:
                pass
            
            #deal with the rest of the form
            new_username=form.cleaned_data['login'].replace('/','').replace('?','')
            print('input',new_username)
            if new_username:
                #check if the username is already taken
                try:
                    lookup=User.objects.filter(username=new_username)[0]
                    #check if the user in question is the logged in user
                    if lookup==request.user:
                        pass
                    else:
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
            
            if form.cleaned_data['display_name']:
                info_obj.display_name=form.cleaned_data['display_name']
                info_obj.save()
            
            
            #return HttpResponseRedirect('/profile/edit/?success=true')
            return HttpResponseRedirect('/profile/?success=true')
        return HttpResponseRedirect('/profile/edit/')
                
    #GET
    form=forms.UserEditForm(initial={
        'email':user_obj.email,
        'login':user_obj.username,
        'display_name':info_obj.display_name
    })
    
    return render(request,'backend/profile_page_edit.html',{'user':request.user,'form':form})

@login_required
def project_list(request):
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            prompt=form.cleaned_data['search']
            return HttpResponseRedirect('/projects/?prompt='+prompt)
        else:
            return HttpResponseRedirect('/projects/')
    form=forms.SearchForm(initial={'search':request.GET.get('prompt','')})
    lookup=find_projects_by_name(request.GET.get('prompt',''))
    return render(request,'backend/project_list.html',{'user':request.user,'lookup':lookup,'form':form,'prompt':request.GET.get('prompt','')})

@login_required
def project_item(request,id):
    proj_obj=models.Project.objects.get(pk=id)
    #check if the logged in user is the author of the project
    is_author=proj_obj.user==request.user
    #verify that the user is allowed to view this page
    allowed_to_see=verify_project_viewing_eligibility(proj_obj,request.user)
    if not allowed_to_see:
        raise PermissionDenied()
    return render(request,'backend/project_item.html',{'user':request.user,'item':proj_obj,
                                                       'is_author':is_author})
    
@login_required
def project_item_edit(request,id):
    proj_obj=models.Project.objects.get(pk=id)
    #check if the logged in user is the author of the project
    is_author=proj_obj.user==request.user
    if not is_author:
        raise PermissionDenied()
    #form time
    if request.method=="POST":
        form=forms.ProfileMetadataForm(request.POST,request.FILES)
        if form.is_valid():
            print(request.FILES)
            print(form.cleaned_data['delete_icon'])
            if request.FILES.get('icon', False) or form.cleaned_data['delete_icon']:
                print('removing icon')
                #remove the old icon
                proj_obj.icon.delete(save=True)
            #see if the need for icon update is be
            if request.FILES.get('icon', False):
                try:
                    proj_obj.icon=form.cleaned_data['icon']
                    extension=proj_obj.icon.name.split('.')[-1]
                    #print(extension)
                    proj_obj.icon.name=str(proj_obj.id)+'.'+extension
                    proj_obj.save()
                except AttributeError:
                    pass
            
            #deal with the rest of the form
            proj_obj.name=form.cleaned_data['name']
            proj_obj.description=form.cleaned_data['description']
            proj_obj.save()
            
            
            #return HttpResponseRedirect('/profile/edit/?success=true')
            return HttpResponseRedirect('/projects/'+str(proj_obj.id)+'/?success=true')
        return HttpResponseRedirect('/projects/'+str(proj_obj.id)+'/metadata_edit/')
                
    #GET
    form=forms.ProfileMetadataForm(initial={
        'name':proj_obj.name,
        'description':proj_obj.description
    })
    
    return render(request,'backend/project_item_edit.html',{'user':request.user,'item':proj_obj,'form':form})

def datastore(request):
    return render(request,'backend/datastore.html',{'user':request.user})