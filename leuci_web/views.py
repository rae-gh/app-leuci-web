from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages.views import SuccessMessageMixin
import plotly.graph_objects as go
import pandas as pd

# ASYNC STUFF
import asyncio
from asgiref.sync import sync_to_async
from time import sleep
import httpx
from typing import List
import random


# my files
from . import sessiondata as sd
from .classes import admin as adm

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

#####################################################################################################################################

from pathlib import Path
import datetime    
import logging 
from django.http import JsonResponse
from asgiref.sync import async_to_sync, sync_to_async

DIR = str(Path(__file__).resolve().parent )+ "/data/"

@sync_to_async
def get_user(request):
    #gl_user = request.user.id    
    gl_user = ""
    gl_ip = str(request.META['REMOTE_ADDR'])
    gl_fwd = ""
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        gl_fwd = str(request.META['HTTP_X_FORWARDED_FOR'])
    gl_rem = str(request.META['REMOTE_ADDR'])
    
    #from ipware import get_client_ip
    #gl_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()    
    #gl_ip, is_routable = get_client_ip(request)
    return gl_user, gl_ip + ":" + gl_fwd + ":" + gl_rem
    
        
async def explore(request):
    context = {
        'pdb_code': "", 
        'resolution':"", 
        'ebi_link':"",
        'exp_method':"",
        'map_header':{},
        'message':"",
        'header_string':"",
         }                
    
    context["full_url"] = await sd.get_url(request, ["pdb_code"])    
    gl_user, gl_ip = await get_user(request)            
    pdb_code, on_file, in_loader, in_interp, mobj = await sd.get_pdbcode_and_status(request)
    if pdb_code == "":
        return render(request, 'explore.html', context)
    print(pdb_code, on_file, in_loader, in_interp)        
    context['pdb_code'] = pdb_code    
    logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' was explored at '+str(datetime.datetime.now())+' hours')
    
    if not on_file:
        context['message'] = "Downloading... "        
        loop = asyncio.get_event_loop()
        async_function = sync_to_async(sd.download_ed, thread_sensitive=False)
        loop.create_task(async_function(request,pdb_code,gl_ip))                                                                
        return render(request, 'explore.html', context)
    elif not in_interp or not in_loader :
        context['message'] = "Uploading... "        
        loop = asyncio.get_event_loop()
        async_function = sync_to_async(sd.upload_ed, thread_sensitive=False)
        loop.create_task(async_function(request,pdb_code,gl_ip))
                                
    if mobj != None:        
        print(mobj)
        context['resolution'] = mobj.resolution
        context['ebi_link'] = mobj.ebi_link
        context['exp_method'] = mobj.exp_method            
        if "x-ray" in mobj.exp_method:        
            context['header_string'] = mobj.header_as_string            
        print("rendering...")
    return render(request, 'explore.html', context)
                        
async def admin(request):
    act = ""
    if 'act' in request.POST:
        act = request.POST.get('act')
    
    context = {}
    gl_user, gl_ip = await get_user(request)
    pdb_code, on_file, in_loader, in_interp, mobj = await sd.get_pdbcode_and_status(request)
    adm_fetch = adm.AdminClass()    
    log_all = False
    if act == "data_show2":
        log_all = True

    if act == "logs_delete":
        context['logs_formatted'] = adm_fetch.delete_logs()
    else:
        context['logs_formatted'] = adm_fetch.show_logs(formatted=True,all=log_all)
    
    if act == "data_delete":
        context['data_formatted'] = adm_fetch.delete_data()
    else:
        context['data_formatted'] = adm_fetch.show_data(formatted=True)
        
    context["pdb_code"]= pdb_code
        
    context["json"] = sd.get_store_info(gl_ip)
                            
    print("rendering...")
    return render(request, 'admin.html', context)

#https://plotly.com/python-api-reference/generated/plotly.graph_objects.Contour.html?highlight=contour#plotly.graph_objects.Contour
async def projection(request):
    context = {}
    context["full_url"] = await sd.get_url(request, ["pdb_code"])
    context['message'] = ""
    # we should already have loaded this asynchronously, too late now if we haven't
    gl_user, gl_ip = await get_user(request)        
    context['pdb_code'] = "dummy"
    logging.info("INFO:\t" + gl_ip + "\t" + "dummy" + ' projection at '+str(datetime.datetime.now())+' hours')
    context["value_check"] = 0
    context["value_len"] = 0                        
    xy = [  [1,2,3,4,5],
        [6,7,8,9,10],
        [0.2,3,8,9,1],
        [0.2,2,2,2,1],
        [0,1,1,1,-2]] 

    from .classes import plotter
    context["plot_div1"] = plotter.makeContour(xy)
    context["plot_div2"] = plotter.makeHeatmap(xy)
    context["plot_div3"] = plotter.makeContour(xy)
            
    print("rendering...")
    return render(request, 'projection.html', context)

async def slice(request):
    context = {}
    context["full_url"] = await sd.get_url(request, ["pdb_code"])
    context['message'] = ""    
    gl_user, gl_ip = await get_user(request)            
    pdb_code, on_file, in_loader, in_interp, mfunc = await sd.get_pdbcode_and_status(request,ret="FUNC")
    context['pdb_code'] = pdb_code    
    if pdb_code == "":
        context['message'] = "Please select a pdb code"   
        return render(request, 'explore.html', context) #return back to choose page

    logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' slice at '+str(datetime.datetime.now())+' hours')
    context["value_check"] = -1
    context["value_len"] = -1
    context["density_mat"] = [[]]
    context["radient_mat"] = [[]]
    context["laplacian_mat"] = [[]]
    if not on_file:
        context['message'] = "Downloading... "        
        loop = asyncio.get_event_loop()
        async_function = sync_to_async(sd.download_ed, thread_sensitive=False)
        loop.create_task(async_function(request,pdb_code,gl_ip))                                                                
    elif not in_interp or not in_loader :
        context['message'] = "Uploading... "        
        loop = asyncio.get_event_loop()
        async_function = sync_to_async(sd.upload_ed, thread_sensitive=False)
        loop.create_task(async_function(request,pdb_code,gl_ip))                                                                                
    elif mfunc == None:
        context['message'] = "Uploading... "        
        loop = asyncio.get_event_loop()
        async_function = sync_to_async(sd.upload_ed, thread_sensitive=False)
        loop.create_task(async_function(request,pdb_code,gl_ip))                                                                                
    else: # then it is in store        
        mobj = mfunc.mobj
        if len(mobj.values) > 0:
            try:
                settings_dic = await sd.get_slice_settings(request)
                for name, val in settings_dic.items():
                    context[name] = val
                interp, centralstr, linearstr, planarstr, width, samples = await sd.get_slice_settings(request)
                context["value_check"] = mobj.values[0]
                context["value_len"] = len(mobj.values)                        
                import leuci_xyz.vectorthree as v3            
                central = v3.VectorThree().from_coords(settings_dic["central"])
                linear = v3.VectorThree().from_coords(settings_dic["linear"])
                planar = v3.VectorThree().from_coords(settings_dic["planar"])         
                vals = mfunc.get_slice(central,linear,planar,int(settings_dic["width"]),int(settings_dic["samples"]),settings_dic["interp"])
                #print(vals)
                        
                #xy = [  [1,2,3,4,5],
                #    [6,7,8,9,10],
                #    [0.2,3,8,9,1],
                #    [0.2,2,2,2,1],
                #    [0,1,1,1,-2]] 

                #print(xy)
                    
                context["density_mat"] = vals
                context["radient_mat"] = vals
                context["laplacian_mat"] = vals
            except:
                context["message"] = "There was an error"
        
    print("rendering...")
    return render(request, 'slice.html', context)

    

async def slice_settings(request):
    """
    The plan for this is it hides all menus and forces the user to return to the view page
    after slecting some settings
    That way all settings are passed in a get-post, sent to slice and stored back in the page
    """
    pdb_code, on_file, in_loader, in_interp, mobj = await sd.get_pdbcode_and_status(request)            
    context = {}
    context['pdb_code'] = pdb_code    
    if pdb_code == "":
        context['message'] = "Please select a pdb code"   
        return render(request, 'explore.html', context) #return back to choose page

    gl_user, gl_ip = await get_user(request)    
    logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' slice settings at '+str(datetime.datetime.now())+' hours')
    print("rendering...")
    settings_dic = await sd.get_slice_settings(request)            
    for name, val in settings_dic.items():
        context[name] = val

    return render(request, 'slice_settings.html', context)
        
        