from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
#from . import models
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
import leuci_xyz.vectorthree as v3 
from leuci_xyz import spacetransform as space
from leuci_map import mapsmanager as mapss

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
    gl_str = ""
    gl_ip = str(request.META['REMOTE_ADDR'])
    gl_str += "RMT-" + gl_ip
    gl_fwd = ""
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        gl_fwd = str(request.META['HTTP_X_FORWARDED_FOR'])
        gl_str += "\tFWD-" + gl_fwd
        
    #from ipware import get_client_ip
    #gl_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()    
    #gl_ip, is_routable = get_client_ip(request)
    return gl_user,  gl_str
    
        
async def explore(request):
    try:
        context = {
            'pdb_code': "", 
            'em_code': "", 
            'resolution':"", 
            'ebi_link':"",
            'em_link':"",
            'exp_method':"",
            'map_header':{},
            'message':"",
            'header_string':"",
            }                
        
        t1 = datetime.datetime.now()
        gl_user, gl_ip = await get_user(request)            
        pdb_code, nav,on_file, in_loader, in_interp, mobj = await sd.get_pdbcode_and_status(request)
        if pdb_code == "":
            return render(request, 'explore.html', context)
        print(pdb_code, on_file, in_loader, in_interp)        
        context['pdb_code'] = pdb_code    
        print("INFO:\t" + gl_ip + "\t" + pdb_code + ' was explored at '+str(datetime.datetime.now())+' hours')
        logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' was explored at '+str(datetime.datetime.now())+' hours')
        
        if not on_file:
            print("Not on file",pdb_code)
            context['message'] = "Downloading... "        
            loop = asyncio.get_event_loop()
            async_function = sync_to_async(sd.download_ed, thread_sensitive=False)
            loop.create_task(async_function(request,pdb_code,gl_ip))
            print("Time taken to start download",datetime.datetime.now()-t1)
            return render(request, 'explore.html', context)
        elif not in_interp or not in_loader or mobj == None :        
            context['message'] = ""       
            mload = sd.upload_ed_header(pdb_code,gl_ip)
            mobj = mload.mobj
                                                    
        if mobj != None:        
            print(mobj)
            context['resolution'] = mobj.resolution
            context['ebi_link'] = mobj.ebi_link
            context['em_link'] = mobj.em_link
            context['em_code'] = mobj.em_code
            context['exp_method'] = mobj.exp_method            
            #if "x-ray" in mobj.exp_method:        
            context['header_string'] = mobj.header_as_string            
            print("rendering...")
        context["full_url"] = await sd.get_url(request,context, ["pdb_code"])    
        print("Time taken",datetime.datetime.now()-t1)
        return render(request, 'explore.html', context)
    except Exception as e:
        context = {}
        context["message"] = str(e)                    
        return render(request, 'error.html', context)
                        
async def admin(request):
    try:
        act = ""
        if 'act' in request.POST:
            act = request.POST.get('act')
        
        context = {}
        gl_user, gl_ip = await get_user(request)
        pdb_code, nav,on_file, in_loader, in_interp, mobj = await sd.get_pdbcode_and_status(request)            
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
            
        #context["json"] = sd.get_store_info(gl_ip)
        context["json"] = mapss.MapsManager().print_maps()
                                    
        print("rendering...")
        return render(request, 'admin.html', context)
    except Exception as e:
        context = {}
        context["message"] = str(e)                    
        return render(request, 'error.html', context)

#https://plotly.com/python-api-reference/generated/plotly.graph_objects.Contour.html?highlight=contour#plotly.graph_objects.Contour
async def cross(request):    
    context = {}
    context['message'] = ""
    gl_user, gl_ip = await get_user(request)
    is_get = await sd.is_get_request(request)
    if is_get:
        print("GET request - synchronous version running for this function")
    pdb_code, nav,on_file, in_loader, in_interp, mfunc = await sd.get_pdbcode_and_status(request,ret="FUNC")
    print("page", pdb_code, nav,on_file, in_loader, in_interp)
    context['pdb_code'] = pdb_code    
    if pdb_code == "":
        context['message'] = "Please select a pdb code"   
        return render(request, 'explore.html', context) #return back to choose page

    print("INFO:\t" + gl_ip + "\t" + pdb_code + ' projection at '+str(datetime.datetime.now())+' hours')    
    logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' projection at '+str(datetime.datetime.now())+' hours')    
    make_slice = True
    if not on_file:
        if is_get:
            sd.download_ed(request,pdb_code,gl_ip)
            pdb_code, nav,on_file, in_loader, in_interp, mfunc = await sd.get_pdbcode_and_status(request,ret="FUNC")
        else:
            make_slice = False
            context['message'] = "Downloading... "        
            loop = asyncio.get_event_loop()
            async_function = sync_to_async(sd.download_ed, thread_sensitive=False)
            loop.create_task(async_function(request,pdb_code,gl_ip))
    elif not in_interp or not in_loader or mfunc == None:
        if True:#is_get:
            sd.upload_ed(pdb_code,gl_ip)
            pdb_code, nav,on_file, in_loader, in_interp, mfunc = await sd.get_pdbcode_and_status(request,ret="FUNC")
        
    if make_slice: # then it is in store and we are going to return a slice view
        settings_dic = await sd.get_cross_settings(request)
        context["pdb_code"] = pdb_code
        lS,lF,lM = settings_dic["layer_xy"],settings_dic["layer_yz"],settings_dic["layer_zx"]        
        lS,lF,lM = max(0,lS),max(0,lF),max(0,lM)
        lS,lF,lM = min(lS,mfunc.mobj.S-1),min(lF,mfunc.mobj.F-1),min(lM,mfunc.mobj.M-1)
        mS,mF,mM = mfunc.mobj.S-1,mfunc.mobj.F-1,mfunc.mobj.M-1

        context["layer_xy"] = lS
        context["layer_yz"] = lF
        context["layer_zx"] = lM
        context["max_xy"] = mS
        context["max_yz"] = mF
        context["max_zx"] = mM
        context["cross_xy"] = mfunc.get_map_cross_section("xy",lS).tolist()
        context["cross_yz"] = mfunc.get_map_cross_section("yz",lF).tolist()
        context["cross_zx"] = mfunc.get_map_cross_section("zx",lM).tolist()
        context["full_url"] = await sd.get_url(request, context,["pdb_code"])    
        return render(request, 'cross.html', context)

async def projection(request):
    context = {}
    context['message'] = ""    
    gl_user, gl_ip = await get_user(request)
    is_get = await sd.is_get_request(request)
    if is_get:
        print("GET request - synchronous version running for this function")
    pdb_code, nav,on_file, in_loader, in_interp, mfunc = await sd.get_pdbcode_and_status(request,ret="FUNC")
    print("page", pdb_code, nav,on_file, in_loader, in_interp)
    context['pdb_code'] = pdb_code    
    if pdb_code == "":
        context['message'] = "Please select a pdb code"   
        return render(request, 'explore.html', context) #return back to choose page

    print("INFO:\t" + gl_ip + "\t" + pdb_code + ' projection at '+str(datetime.datetime.now())+' hours')    
    logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' projection at '+str(datetime.datetime.now())+' hours')    
    make_slice = True
    if not on_file:
        if is_get:
            sd.download_ed(request,pdb_code,gl_ip)
            pdb_code, nav,on_file, in_loader, in_interp, mfunc = await sd.get_pdbcode_and_status(request,ret="FUNC")
        else:
            make_slice = False
            context['message'] = "Downloading... "        
            loop = asyncio.get_event_loop()
            async_function = sync_to_async(sd.download_ed, thread_sensitive=False)
            loop.create_task(async_function(request,pdb_code,gl_ip))
    elif not in_interp or not in_loader or mfunc==None:
        if True:#is_get:
            sd.upload_ed(pdb_code,gl_ip)
            pdb_code, nav,on_file, in_loader, in_interp, mfunc = await sd.get_pdbcode_and_status(request,ret="FUNC")        
            
    if make_slice: # then it is in store and we are going to return a slice view                        
        xs,ys,zs,vs,xx,yy,zz = mfunc.get_atoms_projection("linear",log_level=1)
        context["atoms_x"] = xs
        context["atoms_y"] = ys
        context["atoms_z"] = zs
        context["atoms_v"] = vs
        context["proj_xy"] = mfunc.get_map_projection("xy").tolist()        
        context["proj_yz"] = mfunc.get_map_projection("yz").tolist()
        context["proj_zx"] = mfunc.get_map_projection("zx").tolist()               
        #context["proj_xy_atoms"] = mfunc.get_map_projection("xy",xx[0]-1,xx[1]+1,yy[0]-1,yy[1]+1).tolist()        
        #context["proj_yz_atoms"] = mfunc.get_map_projection("yz",yy[0]-1,yy[1]+1,zz[0]-1,zz[1]+1).tolist()
        #context["proj_zx_atoms"] = mfunc.get_map_projection("zx",xx[0]-1,xx[1]+1,zz[0]-1,zz[1]+1).tolist()        
        context["proj_xy_atoms"] = mfunc.get_map_projection("xy",xx[0],xx[1],yy[0],yy[1]).tolist()        
        context["proj_yz_atoms"] = mfunc.get_map_projection("yz",yy[0],yy[1],zz[0],zz[1]).tolist()
        context["proj_zx_atoms"] = mfunc.get_map_projection("zx",xx[0],xx[1],zz[0],zz[1]).tolist()        
        context["empty"] = []  
        context["x_xy"] = [*range(yy[0],yy[1])]  
        context["y_xy"] = [*range(xx[0],xx[1])]  
        context["x_yz"] = [*range(zz[0],zz[1])]  
        context["y_yz"] = [*range(yy[0],yy[1])]  
        context["x_zx"] = [*range(zz[0],zz[1])]  
        context["y_zx"] = [*range(xx[0],xx[1])]   

        context["full_url"] = await sd.get_url(request, context,["pdb_code"])    
        return render(request, 'projection.html', context)


async def slice(request):
    t1 = datetime.datetime.now()
    ts = datetime.datetime.now()
    try:
        context = {}                
        context['message'] = "" 
        context["messages"] = []
        gl_user, gl_ip = await get_user(request)
        is_get = await sd.is_get_request(request)
        if is_get:
            print("GET request - synchronous version running for this function")
        pdb_code, nav,on_file, in_loader, in_interp, mfunc = await sd.get_pdbcode_and_status(request,ret="FUNC")
        print("page", pdb_code, nav,on_file, in_loader, in_interp)
        context['pdb_code'] = pdb_code    
        if pdb_code == "":
            context['message'] = "Please select a pdb code"   
            return render(request, 'explore.html', context) #return back to choose page

        print("INFO:\t" + gl_ip + "\t" + pdb_code + ' slice at '+str(datetime.datetime.now())+' hours')
        logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' slice at '+str(datetime.datetime.now())+' hours')
        context["value_check"] = -1
        context["value_len"] = -1
        context["density_mat"] = [[]]
        context["radient_mat"] = [[]]
        context["laplacian_mat"] = [[]]
        make_slice = True
        print("Time taken to start check on file",datetime.datetime.now()-t1)
        t1 = datetime.datetime.now()
        if not on_file:
            if is_get:
                sd.download_ed(request,pdb_code,gl_ip)
                pdb_code, nav,on_file, in_loader, in_interp, mfunc = await sd.get_pdbcode_and_status(request,ret="FUNC")
                print("Time taken to start download GET",datetime.datetime.now()-t1)
                t1 = datetime.datetime.now()
            else:
                make_slice = False
                context['message'] = "Downloading... "        
                loop = asyncio.get_event_loop()
                async_function = sync_to_async(sd.download_ed, thread_sensitive=False)
                loop.create_task(async_function(request,pdb_code,gl_ip))
                print("Time taken to start download PUT",datetime.datetime.now()-t1)
                t1 = datetime.datetime.now()
        elif not in_interp or not in_loader or mfunc == None:
            if True:#is_get:
                sd.upload_ed(pdb_code,gl_ip)
                pdb_code, nav,on_file, in_loader, in_interp, mfunc = await sd.get_pdbcode_and_status(request,ret="FUNC")
                print("Time taken to start upload",datetime.datetime.now()-t1)
                t1 = datetime.datetime.now()
                                
        if make_slice: # then it is in store and we are going to return a slice view
            mobj = mfunc.mobj
            pobj = mfunc.pobj
            if len(mobj.values) > 0:
                try:
                    print("getting slice... ")
                    a1,a2,a3 = pobj.get_first_three()
                    keyl,keyc,keyp = pobj.get_key(a1),pobj.get_key(a2),pobj.get_key(a3)
                    cl,cc,cp = pobj.get_coords(a1),pobj.get_coords(a2),pobj.get_coords(a3)                    
                    # defaults from pdb if needed
                    settings_dic = await sd.get_slice_settings(request,[keyc,keyl,keyp],[cc,cl,cp])
                    print("Time taken to get slice settings",datetime.datetime.now()-t1)
                    t1 = datetime.datetime.now()

                    # we need to know some of the settings, the interp and deriv
                    width = int(settings_dic["width"])
                    samples = int(settings_dic["samples"])
                    interp = settings_dic["interp"]
                    deriv = settings_dic["deriv"]                    
                    fo = settings_dic["fo"]
                    fc = settings_dic["fc"]

                    keyc = settings_dic["keyc"]                
                    keyl = settings_dic["keyl"]
                    keyp = settings_dic["keyp"]
                    central = v3.VectorThree().from_coords(settings_dic["central"])
                    linear = v3.VectorThree().from_coords(settings_dic["linear"])
                    planar = v3.VectorThree().from_coords(settings_dic["planar"])                
                                                                    
                    nav = settings_dic["navigate"]                    
                    # the key to finding the slice is the central-linear-planar coordinates                    
                    if nav.upper() == "X": #then we use the given coordinates            
                        pass       
                    elif nav[:2].upper() == "A:":#if nav == "a:" then we use the givern atoms, 0 the given ones, -1 and +1 obvious                                                                                 
                        offset = int(nav[2:])                        
                        print("offset",offset)
                        if offset != 0:
                            keyc = pobj.get_next_key(keyc,offset)
                            keyl = pobj.get_next_key(keyl,offset)
                            keyp = pobj.get_next_key(keyp,offset)
                        print(keyc,keyl,keyp)
                        cc = pobj.get_coords_key(keyc)
                        cl = pobj.get_coords_key(keyl)
                        cp = pobj.get_coords_key(keyp)
                        print(cc,cl,cp)
                        central = v3.VectorThree().from_coords(cc)
                        linear = v3.VectorThree().from_coords(cl)
                        planar = v3.VectorThree().from_coords(cp)
                        print(central.get_key(), linear.get_key(), planar.get_key())
                    elif nav[:2] == "N:":
                        navi = nav[2:]
                        navdis = settings_dic["navdis"]
                        print("Navigatin",navi)
                        spc = space.SpaceTransform(central, linear, planar)
                        central = spc.navigate(central,navi,navdis)
                        linear = spc.navigate(linear,navi,navdis)
                        planar = spc.navigate(planar,navi,navdis)
                                                            
                    atc = pobj.get_atm_key(keyc)                
                    atl = pobj.get_atm_key(keyl)                
                    atp = pobj.get_atm_key(keyp)                                                
                    aac,aal,aap = atc["aa"],atl["aa"],atp["aa"]  
                    context['nav'] = "x"
                    context["aac"] = aac
                    context["aal"] = aal
                    context["aap"] = aap 
                    for name, val in settings_dic.items():
                        context[name] = val                                                
                    context["value_check"] = mobj.values[0]
                    context["value_len"] = len(mobj.values)
                    context["central"] = central.get_key() 
                    context["linear"] = linear.get_key()
                    context["planar"] = planar.get_key()
                    context["keyc"] = keyc
                    context["keyl"] = keyl
                    context["keyp"] = keyp
                    
                    # find the distance from given atoms to given coords
                    cc = v3.VectorThree().from_coords(pobj.get_coords_key(keyc))
                    ll = v3.VectorThree().from_coords(pobj.get_coords_key(keyl))
                    pp = v3.VectorThree().from_coords(pobj.get_coords_key(keyp))
                    context["disc"] = round(cc.distance(central),4)
                    context["disl"] = round(ll.distance(linear),4)
                    context["disp"] = round(pp.distance(planar),4)
                    
                    vals,rads,laps = [[]],[[]],[[]]
                    context["density_mat"] = vals
                    context["radient_mat"] = rads
                    context["laplacian_mat"] = laps

                    context["den_blocknone"] = "" # "display:block"
                    context["rad_blocknone"] = ""
                    context["lap_blocknone"] = ""
                    context["three_blocknone"] = ""
                    context["one_blocknone"] = "display:none;visibility: collapse"
                    context["other_blocknone"] = "display:none;visibility: collapse"

                    print("Time taken to get prepare to get slice",datetime.datetime.now()-t1)
                    t1 = datetime.datetime.now()

                    den_rad_lap = ["mv3","mv5","cubic","bspline"]
                    den_rad = ["mv1","linear"]
                    den_only = ["nearest","numpest"]

                                        
                    if deriv == "three":
                        #vals = mfunc.get_slice(central,linear,planar,width,samples,interp,deriv=0,fo=fo,fc=fc,log_level=1,degree=degree).tolist()
                        vals = mfunc.get_slice(central,linear,planar,width,samples,interp,deriv=0,fo=fo,fc=fc,log_level=1)
                        if settings_dic["interp"] not in den_only:
                            #rads = mfunc.get_slice(central,linear,planar,width,samples,interp,deriv=1,fo=fo,fc=fc,log_level=1,degree=degree).tolist()
                            rads = mfunc.get_slice(central,linear,planar,width,samples,interp,deriv=1,fo=fo,fc=fc,log_level=1)
                            if settings_dic["interp"] in den_rad_lap:
                                #laps = mfunc.get_slice(central,linear,planar,width,samples,interp,deriv=2,fo=fo,fc=fc,log_level=1,degree=degree).tolist()
                                laps = mfunc.get_slice(central,linear,planar,width,samples,interp,deriv=2,fo=fo,fc=fc,log_level=1)
                        context["density_mat"] = vals
                        context["radient_mat"] = rads
                        context["laplacian_mat"] = laps                                                                                    
                    else:                        
                        context["den_blocknone"] = "display:none;visibility: collapse"
                        context["rad_blocknone"] = "display:none;visibility: collapse"
                        context["lap_blocknone"] = "display:none;visibility: collapse"
                        context["three_blocknone"] = "display:none;visibility: collapse"
                        context["other_blocknone"] = "display:none;visibility: collapse"                        
                        if deriv == "density":
                            #vals = mfunc.get_slice(central,linear,planar,width,samples,interp,deriv=0,fo=fo,fc=fc,log_level=1,degree=degree).tolist()
                            vals = mfunc.get_slice(central,linear,planar,width,samples,interp,deriv=0,fo=fo,fc=fc,log_level=1)
                            context["density_mat"] = vals
                            context["den_blocknone"] = ""
                            context["one_blocknone"] = ""
                        elif deriv == "radient":
                            #rads = mfunc.get_slice(central,linear,planar,width,samples,interp,deriv=1,fo=fo,fc=fc,log_level=1,degree=degree).tolist()
                            rads = mfunc.get_slice(central,linear,planar,width,samples,interp,deriv=1,fo=fo,fc=fc,log_level=1)
                            context["radient_mat"] = rads
                            context["rad_blocknone"] = ""
                            context["other_blocknone"] = ""
                        elif deriv == "laplacian":
                            #laps = mfunc.get_slice(central,linear,planar,width,samples,interp,deriv=2,fo=fo,fc=fc,log_level=1,degree=degree).tolist()
                            laps = mfunc.get_slice(central,linear,planar,width,samples,interp,deriv=2,fo=fo,fc=fc,log_level=1)
                            context["laplacian_mat"] = laps
                            context["lap_blocknone"] = ""
                            context["other_blocknone"] = ""                                            
                    
                    print("Time taken to get slice",datetime.datetime.now()-t1)
                    t1 = datetime.datetime.now()                    
                    nybs = settings_dic["naybs"]
                    if nybs == "Y":
                        naybs = mfunc.get_slice_neighbours(central,linear,planar,width,samples,[0,0.5])
                        print("Time taken to get neighbours",datetime.datetime.now()-t1)
                        t1 = datetime.datetime.now()
                    else:
                        naybs = [[]]
                    context["nayb_mat"] = naybs                                                            
                    ## Finally create the position dots if we want them
                    pdots = settings_dic["posdots"]
                    adots = settings_dic["atomdots"]                    
                    print("Dots=",pdots,adots)
                    context["zero_dotsX"] = []
                    context["zero_dotsY"] = []
                    context["posi_dotsX"] = []
                    context["posi_dotsY"] = []                                        
                    context["negi_dotsX"] = []
                    context["negi_dotsY"] = []
                    dots = []
                    if pdots == "Y":
                        dots.append(central)
                        dots.append(linear)
                        dots.append(planar)
                    if adots == "Y":
                        dots.append(cc)
                        dots.append(ll)
                        dots.append(pp)                    
                    if len(dots) > 0:
                        ## Add points to a scatter plot
                        print(samples,width)
                        spc = space.SpaceTransform(central, linear, planar)
                        for dot in dots:
                            posD = spc.reverse_transformation(dot)                        
                            posDp = posD.get_point_pos(samples,width)                                                
                            #print("Dot",posDp.get_key())                                                
                            # The C value will be zero as it is on the plane - that is because these are the points we made the plane with
                            # The xy heatmap has been arranged so the x value is above so linear is upwards, so the y axis (ok a bit confusing.... should I change it)?
                            if posDp.A > 0 and posDp.A < samples and posDp.B > 0 and posDp.B < samples:
                                if abs(posDp.C) < 0.001:
                                    context["zero_dotsX"].append(posDp.B)
                                    context["zero_dotsY"].append(posDp.A)
                                elif posDp.C > 0:
                                    context["posi_dotsX"].append(posDp.B)
                                    context["posi_dotsY"].append(posDp.A)
                                elif posDp.C < 0:
                                    context["negi_dotsX"].append(posDp.B)
                                    context["negi_dotsY"].append(posDp.A)
                                                                                                                              
                    print("Density MAT------")
                    #print(context["density_mat"])
                    print("Time taken to add dots",datetime.datetime.now()-t1)
                    print("rendering... took",datetime.datetime.now()-ts)                    
                    context["full_url"] = await sd.get_url(request,context, ["pdb_code","width","samples","interp", "central","linear","planar","keyc","keyl","keyp","deriv","fo","fc","atomdots","posdots"])    
                    strmsg = "INFO:\t" + gl_ip + "\t" + pdb_code + ' slice time taken '+str(datetime.datetime.now())+' hours is '+ str(datetime.datetime.now()-ts)
                    logging.info(strmsg)
                    context["messages"].append("Time taken " + str(round((datetime.datetime.now()-ts).total_seconds(),3)) + " seconds")
                    return render(request, 'slice.html', context)
                    
                except Exception as e:
                    context["message"] = str(e)                    
                    return render(request, 'error.html', context)
            
        print("Time taken",datetime.datetime.now()-t1)
        print("rendering...")
        context["full_url"] = await sd.get_url(request,context, ["pdb_code","width","samples","interp", "central","linear","planar","keyc","keyl","keyp","deriv","fo","fc","atomdots","posdots"])    
        context["messages"].append("Time taken " + str(round((datetime.datetime.now()-ts).total_seconds(),3)) + " seconds")
        return render(request, 'slice.html', context)
    except Exception as e:
        context["message"] = str(e)                
        return render(request, 'error.html', context)

    

async def slice_settings(request):
    """
    The plan for this is it hides all menus and forces the user to return to the view page
    after slecting some settings
    That way all settings are passed in a get-post, sent to slice and stored back in the page
    """
    pdb_code, nav,on_file, in_loader, in_interp, mobj = await sd.get_pdbcode_and_status(request)            
    context = {}
    context['pdb_code'] = pdb_code    
    if pdb_code == "":
        context['message'] = "Please select a pdb code"   
        return render(request, 'explore.html', context) #return back to choose page

    gl_user, gl_ip = await get_user(request)    
    print("INFO:\t" + gl_ip + "\t" + pdb_code + ' slice settings at '+str(datetime.datetime.now())+' hours')
    logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' slice settings at '+str(datetime.datetime.now())+' hours')
    print("rendering...")
    settings_dic = await sd.get_slice_settings(request)            
    for name, val in settings_dic.items():
        context[name] = val

    return render(request, 'slice_settings.html', context)
        
        