from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

import backend.models as models
import backend.serializers as serializers
import backend.data_processing.registry as registry

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
#TODO: rewrite login_required to dump a 401 if user not authorized
# the frontend will need to preserve the url and redirect to /login with query being the current logged in page


def get_project(request,id):
    '''
    test api to retrieve project metadata info
    '''
    if not request.user.pk: #None if not logged in, returns a value otherwise
        return HttpResponse(status=401)
    #check if exists
    try:
        project = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return HttpResponse(status=404)
    if request.method=='GET':
        #finally, verify whether the user is authorized to view this content
        if project.access=='C' and project.user!=request.user:
            return HttpResponse(status=403)
        serializer=serializers.ProjectSerializer(project)
        return JsonResponse(serializer.data)

def get_user_info(request):
    if not request.user.pk: #None if not logged in, returns a value otherwise
        return HttpResponse(status=401)
    if request.method == 'GET':
        #serializer=serializers.UserSerializer(request.user)
        user_detais=models.UserInfo.objects.filter(user=request.user)[0]
        has_pfp=False
        pfp_path=''
        try:
            pfp_obj=models.UserPFP.objects.filter(user=request.user)[0]
            if pfp_obj.pfp:
                has_pfp=True
                pfp_path=pfp_obj.pfp.name
        except IndexError:
            pass
        #print(type(request.user.pk))
        serializer=serializers.UserExtendedSerializer(data={'pk':request.user.pk,
                                                            'username':request.user.username,
                                                            'display_name':user_detais.display_name,
                                                            'has_pfp':has_pfp,'pfp_path':pfp_path})
        is_valid = serializer.is_valid()
        if not is_valid:
            print('serializer',serializer.errors)
        return JsonResponse(serializer.data)

def upd_proj_date(request,id):
    '''
    test api to retrieve project metadata info
    '''
    if not request.user.pk: #None if not logged in, returns a value otherwise
        return HttpResponse(status=401)
    #check if exists
    try:
        project = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return HttpResponse(status=404)
    if request.method=='GET':
        return HttpResponse(status=400)
    elif request.method=='POST':
        #finally, verify whether the user is authorized to view this content
        if project.user!=request.user:
            return HttpResponse(status=404)
        #serializer=serializers.ProjectSerializer(project)
        project.save() #no changes were made, it just updates the edited
        return HttpResponse(status=201)

def _assemble_info(r_sublist):
    l=[]
    for i in r_sublist.keys():
        info={}
        info['name']=i
        obj=r_sublist[i]()
        info['display_name']=obj.display_name
        info['description']=obj.description
        info['accepts']=obj.accepts
        info['returns']=obj.returns
        info['initial']=obj.initial
        l.append(info)
    return l
    
@api_view()
def get_functions_all(request):
    '''
    Retrieves a list of all functions in the registry
    '''
    l={}
    r=registry.Registry()
    #l['loaders']=r.loaders.keys()
    #l['renderers']=r.renderers.keys()
    #l['processors']=r.processors.keys()
    #l['splitters']=r.splitters.keys()
    #l['models']=r.models.keys()
    l['loaders']=_assemble_info(r.loaders)
    l['renderers']=_assemble_info(r.renderers)
    l['splitters']=_assemble_info(r.splitters)
    l['models']=_assemble_info(r.models)
    return Response(l)

@api_view()
def get_function_info(request,func_name):
    '''
    Retrieves information about a specific function
    '''
    r=registry.Registry()
    obj=r.get_all()[func_name]()
    info={}
    info['display_name']=obj.display_name
    info['type']=obj.type
    info['description']=obj.description
    info['accepts']=obj.accepts
    info['returns']=obj.returns
    info['initial']=obj.initial
    return Response(info)


@api_view()
def get_datastore_items_csv(request):
    '''
    Retrieves a list of all CSV files uploaded into the system and belonging to a user
    '''
    lookup=models.DataFile.objects.filter(user=request.user,filetype='CSV')
    l=[]
    for i in lookup:
        l.append({
            'id':str(i.id),
            'name':i.name,
            'description':i.description
        })
    return Response(l)

@api_view(['POST'])
def accept_csv_load(request,id,order=0):
    updating = request.POST.get('update')
    print('aaa',updating)
    #identify project
    try:
        proj_obj = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return Response(status=404)
    #verify if permitted to edit
    if request.user != proj_obj.user:
        return Response(status=403)
    #handle csv file
    dataset_id=request.POST.get('csv_files')
    print(dataset_id)
    data_obj=models.DataFile.objects.get(id=dataset_id)
    print(data_obj)
    #handle pipeline saving
    params={
        'data_obj':str(data_obj.id),
        'save_as':'df' #temporary definition, should be appointed programmatically so to allow suppliment of additional
    }
    try:
        param_obj=models.FunctionParams.objects.filter(project=proj_obj,order=order)[0]
        if updating=='true':
            print('updating')
            param_obj.info['data_obj']=str(data_obj.id)
            param_obj.save()
        else:
            print('not updating')
            return Response(403) #clashing with existing object
    except IndexError:
        if updating=='update':
            return Response(404)
        else:
            param_obj=models.FunctionParams(project=proj_obj,order=order,func_name='LoadCSV',info=params)
            param_obj.save()
    return Response(status=201)

@api_view()
def get_pipeline(request,id):
    r=registry.Registry()
    f_list=r.get_all()
    #identify project
    try:
        proj_obj = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return Response(status=404)
    lookup=models.FunctionParams.objects.filter(project=proj_obj).order_by('order')
    l=[]
    for i in lookup:
        func_obj=f_list[i.func_name]()
        l.append({
            'name':i.func_name,
            'display_name':func_obj.display_name,
            'description':func_obj.description,
            'params_id':str(i.id),
            'accepts':func_obj.accepts,
            'produces':func_obj.returns
            })
    return Response(l)

@api_view()
def get_params(request,params_id):
    try:
        param_obj=models.FunctionParams.objects.get(id=params_id)
    except models.Project.DoesNotExist:
        return Response(status=404)
    serializer=serializers.FunctionParamsSerializer(param_obj)
    return Response(serializer.data)

@api_view(['POST'])
def delete_params(request,params_id):
    #check if exists
    try:
        param_obj=models.FunctionParams.objects.get(id=params_id)
    except models.DoesNotExist:
        return Response(status=404)
    #check if authorized
    print(request.user)
    if request.user!=param_obj.project.user:
        return Response(status=403)
    #finally, perform the deletion
    param_obj.delete()
    return Response(201)

@api_view(['POST'])
def accept_preprocessor(request,id,order):
    updating = request.POST.get('update')
    #identify project
    try:
        proj_obj = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return Response(status=404)
    #verify if permitted to edit
    if request.user != proj_obj.user:
        return Response(status=403)
    params={
        'accept':'df',
        'produce':'df',
        'in_place':True
    }
    #try:
    #    param_obj=models.FunctionParams.objects.filter(project=proj_obj,order=order)[0]
    #need to do order setting first 
    

@api_view(['POST'])  
def accept_renderer(request,id,order=1):
    updating = request.POST.get('update')
    print('aaaa',updating)
    #identify project
    try:
        proj_obj = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return Response(status=404)
    #verify if permitted to edit
    if request.user != proj_obj.user:
        return Response(status=403)
    params={
        'accept':'df' #temporary definition, should be appointed programmatically so to allow suppliment of additional
    }
    try:
        param_obj=models.FunctionParams.objects.filter(project=proj_obj,order=order)[0]
        if updating=='true':
            print('updating')
            param_obj.save()
        else:
            print('not updating')
            return Response(403) #clashing with existing object
    except IndexError:
        if updating=='update':
            return Response(404)
        else:
            param_obj=models.FunctionParams(project=proj_obj,order=order,func_name='RenderDF',info=params)
            param_obj.save()
    return Response(status=201)
    
@api_view(['POST'])
def invoke_runtime(request,id):
    #identify project
    try:
        proj_obj = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return Response(status=404)
    func_list=models.FunctionParams.objects.filter(project=proj_obj).order_by('order')
    var_store={}
    r=registry.Registry()
    for i in func_list:
        #runtime
        #1. figure out the function type. Loaders don't accept values from var_store
        print(i.func_name,i.info)
        func_obj=r.get_all()[i.func_name]()
        print(func_obj)
        try:
            func_status=models.FunctionStatus.objects.filter(func=i)[0]
        except IndexError:
            func_status=models.FunctionStatus(func=i)
        #mark as being executed
        func_status.status='EX'
        func_status.save()
        if func_obj.type=='loader': #only saves, does not accept
            data_obj=models.DataFile.objects.get(id=i.info['data_obj'])
            var_name_save=i.info['save_as']
            var_store[var_name_save]=func_obj.execute(data_obj)
            func_status.info={
                'saved_as':var_name_save
            }
        elif func_obj.type=='processor': #changes loaded data, both saves and accepts
            var_name_load=i.info['accept']
            var_name_save=i.info['save_as']
            var_store[var_name_save]=func_obj.execute(var_store[var_name_load])
            func_status.info={
                'loaded':var_name_load,
                'saved_as':var_name_save
            }
        elif func_obj.type=='renderer': #only outputs, does not save
            var_name_load=i.info['accept']
            #print(func_obj.execute(var_store[var_name_load]))
            try:
                result_obj=models.RuntimeRenderResult.objects.filter(func_params=i)[0]
            except IndexError:
                result_obj=models.RuntimeRenderResult(func_params=i)
            result_obj.result=func_obj.execute(var_store[var_name_load])
            result_obj.save()
            func_status.info={
                'loaded':var_name_load
            }
            #should go to the frontend but i need to figure out some things
            #log it into the database and let the frontend query it at leizure
        func_status.status='OK'
        func_status.save()
    return Response(status=200)

@api_view()
def get_results(request,id):
    #identify project
    try:
        proj_obj = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return Response(status=404)
    func_list=models.FunctionParams.objects.filter(project=proj_obj).order_by('order')
    #seek the result objects
    #those are only present on renderer functions
    response_list={}
    r=registry.Registry()
    r_list=r.get_all()
    for func_params in func_list: #TODO: optimize with counting the number of renderers
        func_obj=r_list[func_params.func_name]() #dont forget to initialize
        if func_obj.type=='renderer':
            try:
                result_obj=models.RuntimeRenderResult.objects.filter(func_params=func_params)[0]
                response_list[func_params.order]={
                    'name':func_params.func_name,
                    'display_name':func_obj.display_name,
                    'resulting_html':result_obj.result
                }
            except IndexError:
                #object not created yet, skipping
                pass
    return Response(response_list)