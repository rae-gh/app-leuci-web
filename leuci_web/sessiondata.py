"""
RSA - 3rd Feb 2023
This file returns info that the user has in scope during the session anonymously

"""
import datetime    
import logging        
from pathlib import Path
from asgiref.sync import async_to_sync, sync_to_async
import json

DIR = str(Path(__file__).resolve().parent )+ "/data/"

import leuci_map.maploader as moad
from leuci_map import mapobject as mobj
import leuci_map.mapfunctions as mfun

from .classes import store as stor

@sync_to_async
def get_url(request,context,items):
    #http://127.0.0.1:8000/explore?pdb_code=2bf9        
    full_url = request.build_absolute_uri()
    full_url += "?"        
    for item in items:
        #print(item,"in")
        if item in context: 
            full_url += item + "=" + str(context[item]) + "&"                
    return full_url[:-1]

@sync_to_async
def is_get_request(request):
    if 'pdb_code' in request.GET:
        return True
    return False

@sync_to_async
def get_pdbcode_and_status(request, ret="DATA"):
    """
    Returns pdb info from current state or downloads from the ebi
    """
    pdb_code,nav,on_file, in_loader, in_interp,mobj, mfunc = "", "",True,False,False,None,None
    req_session = request.POST
    current_code = ""
    if 'pdb_code' in request.POST:
        pdb_code = request.POST.get('pdb_code').lower()        
    elif 'pdb_code' in request.GET:        
        pdb_code = request.GET.get('pdb_code').lower()        
        req_session = request.GET
    
    if 'pdb_code' in request.session:
        current_code = request.session['pdb_code'].lower()            
        if pdb_code == "":
            pdb_code = current_code    
    
    if 'nav' in req_session:
        nav = req_session.get('nav').lower()        
        
    stre = stor.Store()
    in_loader = stre.exists_loader(pdb_code)
    if in_loader:
        mload,dt = stre.get_loader(pdb_code)
        mobj = mload.mobj
    
    in_interp = stre.exists_interper(pdb_code)
    if in_interp:
        mfunc,dt = stre.get_interper(pdb_code)
        mobj = mfunc.mobj

    if not in_loader:
        mload = moad.MapLoader(pdb_code, directory=DIR, cif=False)
        on_file = mload.exists()
        if on_file and mobj == None:
            mload = moad.MapLoader(pdb_code, directory=DIR)            
            mload.load()
            mobj = mload.mobj
            
            
    #return pdb_code, in_store,exists, mload
    request.session['pdb_code'] = pdb_code        
    if ret == "FUNC":
        return pdb_code, nav,on_file, in_loader, in_interp,mfunc
    else:
        return pdb_code, nav,on_file, in_loader, in_interp,mobj
           
def download_ed(request,pdb_code,gl_ip):    
    print("downloading...")    
    my_pdb = moad.MapLoader(pdb_code, directory=DIR)
    my_pdb.download()
    logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' was downloaded at '+str(datetime.datetime.now())+' hours')
    #upload_ed(request,pdb_code,gl_ip)    
    #import urllib.request
    #urllib.request.urlretrieve(f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdbcode}.ent", filename)

def upload_ed(pdb_code,gl_ip):
    mload = upload_ed_header(pdb_code,gl_ip)
    upload_ed_values(pdb_code,mload, gl_ip)

def upload_ed_header(pdb_code,gl_ip):
    try:
        stre = stor.Store()
        if stre.exists_interper(pdb_code):
            mload,dt = stre.get_interper(pdb_code)
            return mload
        #############################################
        print("uploading header...")        
        import json        
        mload = moad.MapLoader(pdb_code, directory=DIR)        
        mload.load()                                                
        stre.add_loader(pdb_code,mload)
        print("added",pdb_code,"to store")            
        logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' was header uploaded at '+str(datetime.datetime.now())+' hours')
        return mload
    except Exception as e:
        logging.info("ERROR:\t" + gl_ip + "\t" + pdb_code + ' error header uploading ' + str(e) + " " + str(datetime.datetime.now())+' hours')

def upload_ed_values(pdb_code,mload,gl_ip):    
    print("uploading values...")    
    try:                        
        if not mload.wait_for_load(log_level=1):
            mload.load_values(diff=True)
            stre = stor.Store()
            mfunc = mfun.MapFunctions(pdb_code,mload.mobj,mload.pobj, "linear") #the default method is linear
            stre.add_interper(pdb_code,mfunc)        
            print(mload.mobj.map_header["01_NC"],mload.mobj.map_header["02_NR"],mload.mobj.map_header["03_NS"])
            print("FMS=",mload.mobj.F,mload.mobj.M,mload.mobj.S)                    
            logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' valued loaded at '+str(datetime.datetime.now())+' hours')
    except Exception as e:
        logging.info("ERROR:\t" + gl_ip + "\t" + pdb_code + ' error loading values ' + str(e) + " " + str(datetime.datetime.now())+' hours')

def get_interper(pdb_code):
    stre = stor.Store()        
    stre.get_interper(pdb_code)
    
def get_store_info(gl_ip):        
    stre = stor.Store()
    return stre.print_interpers

@sync_to_async
def get_cross_settings(request):
    """
    Returns pdb info from current state or downloads from the ebi
    """
    layer_xy, layer_yz, layer_zx = 5,5,5
    ret_dic = {}
    req_store = request.POST        
    if 'pdb_code' in request.GET:                
        req_store = request.GET
    #print(req_store)
    if 'layer_xy' in req_store:
        layer_xy = req_store['layer_xy']
    if 'layer_yz' in req_store:
        layer_yz = req_store['layer_yz']
    if 'layer_zx' in req_store:
        layer_zx = req_store['layer_zx']
    ret_dic["layer_xy"] = int(layer_xy)
    ret_dic["layer_yz"] = int(layer_yz)
    ret_dic["layer_zx"] = int(layer_zx)
    #print(ret_dic["layer_xy"],ret_dic["layer_yz"],ret_dic["layer_zx"])    
    return ret_dic


@sync_to_async
def get_slice_settings(request,keys = [], coords = []):
    """
    Returns pdb info from current state or downloads from the ebi
    """
    refresh, settings = False,False
    if keys == []:
        keyc,keyl,keyp = "","",""
    else:
        keyc,keyl,keyp = keys[0],keys[1],keys[2]    
    if coords == []:
        central, linear, planar = "(2.884,8.478,4.586)","(3.475,7.761,5.794)","(1.791,9.045,4.633)"
    else:
        central, linear, planar = coords[0],coords[1],coords[2]
    width, samples, interp,deriv,degree = 6,100,"linear","density",3
    fo,fc = 2,-1
    navi,navdis = "x",0.1
    adots,pdots = "Y","Y"

    ret_dic = {}

    req_store = request.POST        
    if 'pdb_code' in request.GET:                
        req_store = request.GET
    #print("tmp TODO", req_store)
    
    if 'width' in req_store:
        width = int(req_store.get('width').lower())
    if "samples" in req_store:
        samples = int(req_store.get('samples').lower())
    if "interp" in req_store:
        interp = req_store.get('interp').lower()
    if "central" in req_store:
        central = req_store.get('central').lower()
    if "linear" in req_store:
        linear = req_store.get('linear').lower()
    if "planar" in req_store:
        planar = req_store.get('planar').lower()
    if "keyc" in req_store:
        keyc = req_store.get('keyc').upper()
    if "keyl" in req_store:
        keyl = req_store.get('keyl').upper()
    if "keyp" in req_store:
        keyp = req_store.get('keyp').upper()
    if "navigate" in req_store:
        navi = req_store.get('navigate')
    if "deriv" in req_store:
        deriv = req_store.get('deriv')
    if "degree" in req_store:
        degree = req_store.get('degree')
    if "fo" in req_store:
        fo = int(req_store.get('fo'))
    if "fc" in req_store:
        fc = int(req_store.get('fc'))
    if "atomdots" in req_store:
        adots = req_store.get('atomdots')
    if "posdots" in req_store:
        pdots = req_store.get('posdots')
    if "navdis" in req_store:
        navdis = float(req_store.get('navdis'))
    
    ret_dic["width"] = width
    ret_dic["samples"] = samples
    ret_dic["interp"] = interp
    ret_dic["central"] = central
    ret_dic["linear"] = linear
    ret_dic["planar"] = planar
    ret_dic["keyc"] = keyc
    ret_dic["keyl"] = keyl
    ret_dic["keyp"] = keyp
    ret_dic["navigate"] = navi
    ret_dic["deriv"] = deriv
    ret_dic["degree"] = degree
    ret_dic["fo"] = fo
    ret_dic["fc"] = fc
    ret_dic["atomdots"] = adots
    ret_dic["posdots"] = pdots
    ret_dic["navdis"] = navdis
    
    return ret_dic

    
                
            
    
    
