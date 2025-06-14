from django.shortcuts import render

# Create your views here.
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden, FileResponse, JsonResponse, HttpResponseNotAllowed
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
    project_pins=[]
    lookup=models.ProjectPin.objects.filter(user=request.user).order_by('-created_at')
    for i in lookup:
        project_pins.append(i.project)
    #latest datastore upload
    datastore=models.DataFile.objects.filter(user=request.user).order_by('-last_edited')
    try:
        data_obj=[datastore[0]]
    except IndexError:
        data_obj=[]
    return render(request,'backend/home.html',{'user':request.user,'project_pins':project_pins,'data_obj':data_obj})

@login_required
def profile_page_redirect(request):
    username=request.user.username
    return HttpResponseRedirect('/profile/'+username+'/')
@login_required
def profile_page(request,username):
    is_author=(request.user.username==username)
    user_obj=User.objects.filter(username=username)[0]
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            prompt=form.cleaned_data['search']
            return HttpResponseRedirect('/profile/'+username+'/?prompt='+prompt)
        else:
            return HttpResponseRedirect('/profile/'+username+'/')
    form=forms.SearchForm(initial={'search':request.GET.get('prompt','')})
    prompt=request.GET.get('prompt','')
    if is_author:
        #lookup should include private and unlisted projects
        if prompt:
            lookup=models.Project.objects.filter(user=user_obj,name__icontains=prompt).order_by('-last_edited')
            #get user's stuff
        else:
            lookup=models.Project.objects.filter(user=user_obj).order_by('-last_edited')
    else:  
        #only output public ones
        if prompt:
            lookup=models.Project.objects.filter(user=user_obj,name__icontains=prompt,access='A').order_by('-last_edited')
            #get user's stuff
        else:
            lookup=models.Project.objects.filter(user=user_obj,access='A').order_by('-last_edited')
    return render(request,'backend/profile_page.html',{'user':user_obj,'lookup':lookup,'form':form,'prompt':prompt,'is_author':is_author})

@login_required
def profile_page_edit(request,username):
    if username!=request.user.username:
        return HttpResponseForbidden()
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
                        return HttpResponseRedirect('/profile/'+username+'/edit/?username_taken=true')
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
                    return HttpResponseRedirect('/profile/'+username+'/edit/?wrong_password=true')
                if new_password==verify_password:
                    user_obj.set_password(new_password)
                else:
                    return HttpResponseRedirect('/profile/'+username+'/edit/?password_mismatch=true')

            user_obj.save()
            
            if form.cleaned_data['display_name']:
                info_obj.display_name=form.cleaned_data['display_name']
                info_obj.save()
            
            
            #return HttpResponseRedirect('/profile/edit/?success=true')
            return HttpResponseRedirect('/profile/?success=true')
        return HttpResponseRedirect('/profile/'+username+'/edit/')
                
    #GET
    form=forms.UserEditForm(initial={
        'email':user_obj.email,
        'login':user_obj.username,
        'display_name':info_obj.display_name
    })
    
    return render(request,'backend/profile_page_edit.html',{'user':request.user,'form':form,'has_pfp':bool(pfp_obj.pfp),
                                                            'password_mismatch':request.GET.get('password_mismatch'),
                                                            'username_taken':request.GET.get('username_taken'),
                                                            'wrong_password':request.GET.get('wrong_password')})

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
    lookup=find_projects_by_name(request.GET.get('prompt',''),only_public=True,user=request.user)
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
    #pin handling
    #POST
    if request.method=='POST':
        try:
            pin_obj=models.ProjectPin.objects.filter(user=request.user,project=proj_obj)[0]
            #pin exists, remove it
            pin_obj.delete()
        except IndexError:
            #no pin exists, create one
            pin_obj=models.ProjectPin(user=request.user,project=proj_obj)
            pin_obj.save()
        return HttpResponseRedirect('./')
    #GET
    #is_pinned=False
    try:
        pin_obj=models.ProjectPin.objects.filter(user=request.user,project=proj_obj)[0]
        #if pin_obj exists then the object is pinned
        is_pinned=True
    except IndexError:
        #not pinned
        is_pinned=False
        
    return render(request,'backend/project_item.html',{'user':request.user,'item':proj_obj,
                                                       'is_author':is_author,'is_pinned':is_pinned})
    
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
            proj_obj.access=form.cleaned_data['access']
            proj_obj.description=form.cleaned_data['description']
            proj_obj.save()
            
            
            #return HttpResponseRedirect('/profile/edit/?success=true')
            return HttpResponseRedirect('/projects/'+str(proj_obj.id)+'/?success=true')
        return HttpResponseRedirect('/projects/'+str(proj_obj.id)+'/metadata_edit/')
                
    #GET
    form=forms.ProfileMetadataForm(initial={
        'name':proj_obj.name,
        'access':proj_obj.access,
        'description':proj_obj.description
    })


    return render(request,'backend/project_item_edit.html',{'user':request.user,'item':proj_obj,'form':form,'has_icon':bool(proj_obj.icon)})

@login_required
def project_item_new(request):
    proj_obj=models.Project()
    #POST
    if request.method=="POST":
        form=forms.ProfileMetadataForm(request.POST,request.FILES)
        if form.is_valid():
            print(request.FILES)
            if request.FILES.get('icon', False): #returns an icon or false if none is provided
                try:
                    proj_obj.icon=form.cleaned_data['icon']
                    extension=proj_obj.icon.name.split('.')[-1]
                    #print(extension)
                    proj_obj.icon.name=str(proj_obj.id)+'.'+extension
                    proj_obj.save()
                except AttributeError:
                    pass
            
            #deal with the rest of the form
            proj_obj.user=request.user
            proj_obj.name=form.cleaned_data['name']
            proj_obj.access=form.cleaned_data['access']
            proj_obj.description=form.cleaned_data['description']
            proj_obj.save()
            return HttpResponseRedirect('/projects/'+str(proj_obj.id)+'/?success=true')
        return HttpResponseRedirect('/projects/new/')
    #GET
    form=forms.ProfileMetadataForm()
    #set names for the dummy project thumb (do not save!)
    proj_obj.name='New Project'
    proj_obj.user=request.user
    return render(request,'backend/project_item_new.html',{'user':request.user,'item':proj_obj,'form':form})
    
@login_required
def project_item_delete(request,id):
    proj_obj=models.Project.objects.get(pk=id)
    if proj_obj.user != request.user:
        raise PermissionDenied()
    #do the query handling here
    if request.GET.get('confirm',''):
        #commence the deletion
        proj_obj.icon.delete(save=True) #should get rid of the file
        proj_obj.delete()
        return HttpResponseRedirect('/projects/')
        
    return render(request,'backend/project_item_delete.html',{'user':request.user,'item':proj_obj})

@login_required
def datastore(request):
    #POST
    if request.method=='POST':
        data_obj=models.DataFile(user=request.user)
        form=forms.DataFileForm(request.POST,request.FILES,instance=data_obj)
        if form.is_valid():
            #print(request.FILES)
            #assuming that the file is indeed supplied because the file field is set to be required
            #data_obj=form.save(commit=False)
            #data_obj.user=request.user
            #data_obj.file=form.cleaned_data['file']
            #form supported extensions list
            #TODO: rewrite to use mimetypes instead of file extensions
            extension=data_obj.file.name.split('.')[-1]
            e=models.DataFile.EXTENSIONS
            if '.'+extension in e.values():
                pass
            else:
                return HttpResponseNotAllowed([])
            #the following might be better suited in DataFile.save() method instead
            data_obj.filetype=list(e.keys())[list(e.values()).index('.'+extension)]
            data_obj.file.name=str(data_obj.id)+'.'+extension
            form.save()
            #data_obj.save()
            return HttpResponseRedirect('/datastore/?success=true')
    #GET
    form=forms.DataFileForm()
    lookup=models.DataFile.objects.filter(user=request.user)
    return render(request,'backend/datastore.html',{'user':request.user,'form':form,'lookup':lookup})

@login_required
def datastore_item(request,id):
    data_obj=models.DataFile.objects.get(pk=id)
    if data_obj.user != request.user:
        #unauthorized
        raise PermissionDenied()
    
    return render(request,'backend/datastore_item.html',{'user':request.user,'item':data_obj})

@login_required
def datastore_edit(request,id):
    data_obj=models.DataFile.objects.get(pk=id)
    if data_obj.user != request.user:
        #unauthorized
        raise PermissionDenied()
    #POST
    if request.method=='POST':
        form=forms.DataFileUPDForm(request.POST,instance=data_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/datastore/'+str(data_obj.id)+'/?success=true')
    #GET
    form=forms.DataFileUPDForm(instance=data_obj)
    return render(request,'backend/datastore_item_edit.html',{'user':request.user,'item':data_obj,'form':form})

@login_required
def datastore_delete(request,id):
    data_obj=models.DataFile.objects.get(pk=id)
    if data_obj.user != request.user:
        #unauthorized
        raise PermissionDenied()
    #do the query handling here
    if request.GET.get('confirm',''):
        #commence the deletion
        data_obj.file.delete(save=True)
        data_obj.delete()
        return HttpResponseRedirect('/datastore/')
        
    return render(request,'backend/datastore_item_delete.html',{'user':request.user,'item':data_obj})