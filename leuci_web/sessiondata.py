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


#import leuci_map.maploader as moad
from leuci_map import mapobject as mobj
import leuci_map.mapfunctions as mfun
from leuci_map import mapsmanager as mapss
mapss.MapsManager().set_dir(DIR)

#from .classes import store as stor

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
    pdb_code,nav,on_file, in_loader, in_interp,mobj, mfunc = "", "",False,False,False,None,None
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
                
    mload = mapss.MapsManager().get_or_create(pdb_code,file=0,header=0,values=0)    
    if mload.exists() and mload.em_loaded:
        print("exists already")
        mobj = mload.mobj
        mfunc = mfun.MapFunctions(pdb_code,mload.mobj,mload.pobj, "linear") #the default method is linear
    
    if mload.exists():
        on_file = True
    if mload.em_loaded:
        in_loader = True
    if mload.values_loaded:
        in_interp = True
                                
    #return pdb_code, in_store,exists, mload
    print("return",pdb_code, nav,on_file, in_loader, in_interp)
    request.session['pdb_code'] = pdb_code        
    if ret == "FUNC":
        return pdb_code, nav,on_file, in_loader, in_interp,mfunc
    else:
        return pdb_code, nav,on_file, in_loader, in_interp,mobj

           
def download_ed(request,pdb_code,gl_ip):    
    print("downloading...",pdb_code)    
    #my_pdb = moad.MapLoader(pdb_code, directory=DIR)
    #my_pdb.download()
    mload = mapss.MapsManager().get_or_create(pdb_code,file=1,header=0,values=0)
    logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' was downloaded at '+str(datetime.datetime.now())+' hours')
    #upload_ed(request,pdb_code,gl_ip)    
    #import urllib.request
    #urllib.request.urlretrieve(f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdbcode}.ent", filename)

def upload_ed(pdb_code,gl_ip):
    mload = upload_ed_header(pdb_code,gl_ip)
    upload_ed_values(pdb_code,mload, gl_ip)

def upload_ed_header(pdb_code,gl_ip):
    try:        
        #############################################
        print("uploading header...")        
        import json        
        #mload = moad.MapLoader(pdb_code, directory=DIR)
        mload = mapss.MapsManager().get_or_create(pdb_code,file=1,header=1,values=0)
        mload.load()                                                        
        print("added",pdb_code,"to store")            
        logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' was header uploaded at '+str(datetime.datetime.now())+' hours')
        return mload
    except Exception as e:
        logging.info("ERROR:\t" + gl_ip + "\t" + pdb_code + ' error header uploading ' + str(e) + " " + str(datetime.datetime.now())+' hours')

def upload_ed_values(pdb_code,mload,gl_ip):    
    print("uploading values...")    
    try:
        mload = mapss.MapsManager().get_or_create(pdb_code,file=1,header=1,values=1)                                            
        mfunc = mfun.MapFunctions(pdb_code,mload.mobj,mload.pobj, "linear") #the default method is linear            
        print(mload.mobj.map_header["01_NC"],mload.mobj.map_header["02_NR"],mload.mobj.map_header["03_NS"])
        print("FMS=",mload.mobj.F,mload.mobj.M,mload.mobj.S)                    
        logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' valued loaded at '+str(datetime.datetime.now())+' hours')
    except Exception as e:
        logging.info("ERROR:\t" + gl_ip + "\t" + pdb_code + ' error loading values ' + str(e) + " " + str(datetime.datetime.now())+' hours')

   
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
    width, samples, interp,deriv = 6,50,"linear","density"
    fo,fc = 2,-1
    navi,navdis = "x",0.1
    adots,pdots = "Y","N"
    naybs = "N"

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
    if "neighbours" in req_store:
        naybs = req_store.get('neighbours')
    
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
    ret_dic["fo"] = fo
    ret_dic["fc"] = fc
    ret_dic["atomdots"] = adots
    ret_dic["posdots"] = pdots
    ret_dic["navdis"] = navdis
    ret_dic["naybs"] = naybs
    
    return ret_dic

    
                
            
    
    
