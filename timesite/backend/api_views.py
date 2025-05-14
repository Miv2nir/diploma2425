from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

import backend.models as models
import backend.serializers as serializers
import backend.data_processing.registry as registry

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
import json
from timesite.settings import MEDIA_ROOT
import pathlib

import traceback

from time import sleep
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
    
@api_view()
def get_specific_user_info(request,pk):
    user=User.objects.get(pk=pk)
    try:
        user_detais=models.UserInfo.objects.get(pk=pk)
    except models.UserInfo.DoesNotExist:
        return Response(status=404)
    has_pfp=False
    pfp_path=''
    try:
        pfp_obj=models.UserPFP.objects.filter(user=user)[0]
        if pfp_obj.pfp:
            has_pfp=True
            pfp_path=pfp_obj.pfp.name
    except IndexError:
        pass
    serializer=serializers.UserExtendedSerializer(data={'pk':user.pk,
                                                        'username':user.username,
                                                        'display_name':user_detais.display_name,
                                                        'has_pfp':has_pfp,'pfp_path':pfp_path})
    is_valid = serializer.is_valid()
    if not is_valid:
        print('serializer',serializer.errors)
    return Response(serializer.data)
    

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
    l['processors']=_assemble_info(r.processors)
    #l['splitters']=_assemble_info(r.splitters)
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

@api_view()
def get_foreign_datastore_item(request,func_id):
    '''
    Retrieves a name of a datastore item used in a pipeline for the guest mode
    '''
    func_obj=models.FunctionParams.objects.get(id=func_id)
    data_obj=models.DataFile.objects.get(id=func_obj.info['data_obj'])
    if data_obj.display_in_guest_mode:
        return Response(data_obj.name)
    else:
        return Response(status=403)

@api_view(['POST'])
def accept_csv_load(request,id):
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
    print('test',request.POST.get('var_name'))
    #handle pipeline saving
    if request.POST.get('var_name'):
        save_as=request.POST.get('var_name')
    else:
        save_as='df'
    params={
        'data_obj':str(data_obj.id),
        #'save_as':'df' #temporary definition, should be appointed programmatically so to allow suppliment of additional
        'save_as':save_as
    }
    #get order from the frontend
    order=request.POST.get('order')
    print('order:',order)
    if order==None: #new object
        order=len(models.FunctionParams.objects.filter(project=proj_obj))
    else: #updating
        pass
    print('order:',order)
    try:
        param_obj=models.FunctionParams.objects.filter(project=proj_obj,order=order)[0]
        print('param_obj',param_obj)
        if updating=='true':
            print('updating')
            #param_obj.info['data_obj']=str(data_obj.id)
            param_obj.info=params
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
        try:
            produces=i.info['save_as']
        except KeyError:
            produces=func_obj.returns
            
        try:
            accepts=i.info['accept']
        except KeyError:
            accepts=func_obj.accepts
        l.append({
            'name':i.func_name,
            'display_name':func_obj.display_name,
            'type':func_obj.type,
            'description':func_obj.description,
            'params_id':str(i.id),
            'accepts':accepts,
            'produces':produces
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
    proj_obj=param_obj.project
    #log the order to shift other functions accordingly
    old_order=param_obj.order
    if request.user!=param_obj.project.user:
        return Response(status=403)
    #finally, perform the deletion
    if param_obj.func_name=='DownloadDF': #nuke the file if exists
        path_to_file=MEDIA_ROOT+'temp/'+str(param_obj.id)+'.csv'
        target_file=pathlib.Path(path_to_file)
        target_file.unlink(missing_ok=True)
        print(path_to_file)
    param_obj.delete()
    #move the remaining objects back
    for i in models.FunctionParams.objects.filter(project=proj_obj,order__gt=old_order):
        i.order-=1
        i.save()
    return Response(201)

@api_view(['POST'])
def accept_processor(request,id):
    updating = request.POST.get('update')
    print(updating)
    #identify project
    try:
        proj_obj = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return Response(status=404)
    #verify if permitted to edit
    if request.user != proj_obj.user:
        return Response(status=403)
    #determine the object
    func_name=request.POST.get('func_name')
    print(func_name)
    if func_name=='DropColumns':
        params_string=request.POST.get('text_params') #rewrite to work with the new mode
        params_dict={'text_params':params_string}
    elif func_name=='FillNA':
        params_dict={'fill_mode':request.POST.get('fill_mode')}
        if request.POST.get('fill_mode')=='value':
            pass #save the value
            params_dict['value']=request.POST.get('fill_value')
    elif func_name=='GetQuantile':
        #params_dict['quantile']=request.POST.get('q')
        #params_dict['numeric_only']=request.POST.get('numeric_only')
        params_dict={
            'quantile':request.POST.get('q'),
            'numeric_only':request.POST.get('numeric_only')
        }
    else:
        params_dict={}
    if request.POST.get('load_var_name'):
        accept=request.POST.get('load_var_name')
    else:
        accept='df'
    if request.POST.get('save_var_name'):
        save_as=request.POST.get('save_var_name')
    else:
        save_as='df'
    params={
        'accept':accept,
        'save_as':save_as,
        'in_place':True,
        'params_type':'dict',
        'params':params_dict
    }
    order=request.POST.get('order')
    print('order:',order)
    if order==None: #new object
        order=len(models.FunctionParams.objects.filter(project=proj_obj))
    else: #updating
        pass
    print('order:',order)
    #order=len(models.FunctionParams.objects.filter(project=proj_obj))
    try:
        param_obj=models.FunctionParams.objects.filter(project=proj_obj,order=order)[0]
        if updating=='true':
            print('existing object, updating')
            param_obj.info=params
            param_obj.save()
        else:
            print('existing object, not updating')
            return Response(403) #clashing with existing object
    except IndexError:
        if updating=='update':
            return Response(404)
        else:
            print('new object, creating')
            param_obj=models.FunctionParams(project=proj_obj,order=order,func_name=func_name,info=params)
            param_obj.save()
    return Response(status=201)
    

@api_view(['POST'])  
def accept_renderer(request,id):
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
    params_dict={}
    if request.POST.get('load_var_name'):
        accept=request.POST.get('load_var_name')
    else:
        accept='df'
    params={
        'accept':accept, #temporary definition, should be appointed programmatically so to allow suppliment of additional
        'params_type':'dict',
        'params':params_dict
    }
    #determine the object
    func_name=request.POST.get('func_name')
    #DownloadDF needs a reference onto the function object for setting the file name
    def download_df_treatment(params_dict,param_obj):
        if func_name=='DownloadDF':
            params_dict['params_id']=str(param_obj.id)
        return params_dict
    #handle the rest of the form
    if func_name=='DownloadDF':
        params_dict['index']=request.POST.get('index_toggle')
    
    #determine function order
    order=request.POST.get('order')
    print('order:',order)
    if order==None: #new object
        order=len(models.FunctionParams.objects.filter(project=proj_obj))
    else: #updating
        pass
    print('order:',order)
    #order=len(models.FunctionParams.objects.filter(project=proj_obj))
    try:
        param_obj=models.FunctionParams.objects.filter(project=proj_obj,order=order)[0]
        if updating=='true':
            print('existing object, updating')
            params_dict=download_df_treatment(params_dict,param_obj)
            param_obj.info=params
            param_obj.save()
        else:
            print('existing object, not updating')
            return Response(403) #clashing with existing object
    except IndexError:
        if updating=='update':
            return Response(404)
        else:
            print('new object, creating')
            param_obj=models.FunctionParams(project=proj_obj,order=order,func_name=func_name,info=params)
            params_dict=download_df_treatment(params_dict,param_obj)
            param_obj.info=params
            param_obj.save()
    return Response(status=201)
    
@api_view(['POST'])
def accept_model(request,id):
    updating = request.POST.get('update')
    print(updating)
    #identify project
    try:
        proj_obj = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return Response(status=404)
    #verify if permitted to edit
    if request.user != proj_obj.user:
        return Response(status=403)
    #determine the object
    func_name=request.POST.get('func_name')
    print(func_name)
    if func_name=='FloatPointEvolModelFit':
        #one part of the integrated model work, produces a dictionary with parameters
        params_dict={
            'chosen_column':request.POST.get('chosen_column'),
            'p':request.POST.get('p'),
            'q':request.POST.get('q'),
            'jump_threshold':request.POST.get('jump_threshold')
        }
    else:
        params_dict={}
    if request.POST.get('load_var_name'):
        accept=request.POST.get('load_var_name')
    else:
        accept='df'
    if request.POST.get('save_var_name'):
        save_as=request.POST.get('save_var_name')
    else:
        save_as='df'
    params={
        'accept':accept,
        'save_as':save_as,
        'in_place':True,
        'params_type':'dict',
        'params':params_dict
    }
    order=request.POST.get('order')
    print('order:',order)
    if order==None: #new object
        order=len(models.FunctionParams.objects.filter(project=proj_obj))
    else: #updating
        pass
    print('order:',order)
    try:
        param_obj=models.FunctionParams.objects.filter(project=proj_obj,order=order)[0]
        if updating=='true':
            print('existing object, updating')
            param_obj.info=params
            param_obj.save()
        else:
            print('existing object, not updating')
            return Response(403) #clashing with existing object
    except IndexError:
        if updating=='update':
            return Response(404)
        else:
            print('new object, creating')
            param_obj=models.FunctionParams(project=proj_obj,order=order,func_name=func_name,info=params)
            param_obj.save()
    return Response(status=201)

@api_view(['POST'])
def invoke_runtime(request,id):
    #identify project
    try:
        proj_obj = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return Response(status=404)
    #verify if permitted to edit (non-authors should only be able to get the results)
    if request.user != proj_obj.user:
        return Response(status=403)
    func_list=models.FunctionParams.objects.filter(project=proj_obj).order_by('order')
    var_store={}
    r=registry.Registry()
    #before this, remove all the log objects and create new ones
    for i in func_list:
        try:
            status_obj=i.functionstatus
            status_obj.delete()
            #making a new one
            models.FunctionStatus(func=i).save()
        except ObjectDoesNotExist:
            pass
    for i in func_list:
        #runtime logic goes here
        #1. figure out the function type. Loaders don't accept values from var_store
        print(i.func_name,i.info)
        func_obj=r.get_all()[i.func_name]()
        print('Func_Obj:',func_obj)
        try:
            func_status=models.FunctionStatus.objects.filter(func=i)[0]
        except IndexError:
            func_status=models.FunctionStatus(func=i)
        #mark as being executed
        func_status.status='EX'
        func_status.save()
        #sleep(1.5)
        try:
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
                try:
                    params=i.info['params']
                except KeyError:
                    params={}
                var_store[var_name_save]=func_obj.execute(var_store[var_name_load],params)
                func_status.info={
                    'loaded':var_name_load,
                    'saved_as':var_name_save
                }
            elif func_obj.type=='renderer': #only outputs, does not save
                var_name_load=i.info['accept']
                try:
                    params=i.info['params']
                except KeyError:
                    params={}
                #print(func_obj.execute(var_store[var_name_load]))
                try:
                    result_obj=models.RuntimeRenderResult.objects.filter(func_params=i)[0]
                except IndexError:
                    result_obj=models.RuntimeRenderResult(func_params=i)
                print('test',func_obj)
                result_obj.result=func_obj.execute(var_store[var_name_load],params)
                result_obj.save()
                func_status.info={
                    'loaded':var_name_load
                }
                
            
            func_status.status='OK'
            func_status.save()
        except Exception as e: 
            print(traceback.format_exc())
            func_status.status='ER'
            func_status.info={
                'error':repr(e)
            }
            func_status.save()
            return Response(status=500)
        #for the purposes of testing the RuntimeQueryer.svelte
        #sleep(1.5)
    return Response(status=200)

@api_view()
def get_runtime_status(request,id):
    #identify project
    try:
        proj_obj = models.Project.objects.get(pk=id)
    except models.Project.DoesNotExist:
        return Response(status=404)
    func_list=models.FunctionParams.objects.filter(project=proj_obj).order_by('order')
    #seek out the status objects
    status_list=[]
    for i in func_list:
        try:
            s=serializers.FunctionStatusSerializer(i.functionstatus).data
            s['func_name']=i.func_name
            status_list.append(s)
        except ObjectDoesNotExist:
            pass
    print(status_list)
    #serialize the list
    return Response(status_list)

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

#they just want your hands moving up & down :D

@api_view(['POST'])
def move_function_up(request,func_id):
    #identify project
    params_obj=models.FunctionParams.objects.get(id=func_id)
    proj_obj=params_obj.project
    #verify if permitted to edit
    if request.user != proj_obj.user:
        return Response(status=403)
    #get the target function
    params_obj=models.FunctionParams.objects.get(id=func_id)
    try:
        next_params_obj=models.FunctionParams.objects.filter(project=proj_obj,order=params_obj.order+1)[0]
    except IndexError:
        #no superseeding function found
        return Response(status=200)
    next_params_obj.order-=1
    next_params_obj.save()
    params_obj.order+=1
    params_obj.save()
    return Response(status=201)
    

@api_view(['POST'])
def move_function_down(request,func_id):
    #identify project
    params_obj=models.FunctionParams.objects.get(id=func_id)
    proj_obj=params_obj.project
    #verify if permitted to edit
    if request.user != proj_obj.user:
        return Response(status=403)
    #get the target function
    try:
        previous_params_obj=models.FunctionParams.objects.filter(project=proj_obj,order=params_obj.order-1)[0]
    except IndexError:
        #no superseeding function found
        return Response(status=200)
    previous_params_obj.order+=1
    previous_params_obj.save()
    params_obj.order-=1
    params_obj.save()
    return Response(status=201)
    