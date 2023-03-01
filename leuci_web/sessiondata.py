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

import leuci_map.mapobject as mobj
import leuci_map.maploader as moad
import leuci_map.mapfunctions as mfun

from .classes import store as stor

@sync_to_async
def get_url(request,items):
    #http://127.0.0.1:8000/explore?pdb_code=2bf9        
    full_url = request.build_absolute_uri()
    full_url += "?"
    store = {}
    if request.method =='POST':
        store = request.POST
    elif request.method =='GET':
        store = request.GET
    for item in items:        
        if item in store: 
            full_url += item + "=" + store.get(item) + "&"
        
    return full_url[:-1]

@sync_to_async
def get_pdbcode_and_status(request, ret="DATA"):
    """
    Returns pdb info from current state or downloads from the ebi
    """
    pdb_code,on_file, in_loader, in_interp,mobj, mfunc = "", True,False,False,None,None
    current_code = ""
    if 'pdb_code' in request.POST:
        pdb_code = request.POST.get('pdb_code').lower()        
    elif 'pdb_code' in request.GET:
        pdb_code = request.GET.get('pdb_code').lower()        
    if 'pdb_code' in request.session:
        current_code = request.session['pdb_code'].lower()            
        if pdb_code == "":
            pdb_code = current_code    
    
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
        return pdb_code, on_file, in_loader, in_interp,mfunc
    else:
        return pdb_code, on_file, in_loader, in_interp,mobj

                   
def download_ed(request,pdb_code,gl_ip):    
    print("downloading...")    
    my_pdb = moad.MapLoader(pdb_code, directory=DIR)
    my_pdb.download()
    logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' was downloaded at '+str(datetime.datetime.now())+' hours')
    upload_ed(request,pdb_code,gl_ip)
    #import urllib.request
    #urllib.request.urlretrieve(f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdbcode}.ent", filename)

def upload_ed(request,pdb_code,gl_ip):    
    print("uploading...")    
    try:
        import json
        mload = moad.MapLoader(pdb_code, directory=DIR)
        mload.load()
        mload.load_values()           
        mload.load_values(diff=True)    
        mfunc = mfun.MapFunctions(pdb_code,mload.mobj, "linear") #the default method is linear
        stre = stor.Store()        
        stre.add_interper(pdb_code,mfunc)
        stre.add_loader(pdb_code,mload)
        print("added",pdb_code,"to store")            
        logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' was uploaded at '+str(datetime.datetime.now())+' hours')
    except:
        logging.info("ERROR:\t" + gl_ip + "\t" + pdb_code + ' error uploading '+str(datetime.datetime.now())+' hours')

def get_interper(pdb_code):
    stre = stor.Store()        
    stre.get_interper(pdb_code)
    
def get_store_info(gl_ip):        
    stre = stor.Store()
    return stre.print_interpers

@sync_to_async
def get_slice_settings(request):
    """
    Returns pdb info from current state or downloads from the ebi
    """
    refresh, settings = False,False
    width, samples, interp, central, linear, planar = 6,20,"linear","(2.884,8.478,4.586)","(3.475,7.761,5.794)","(1.791,9.045,4.633)"

    ret_dic = {}
    
    req_store = request.POST
    if 'width' in request.POST:
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
    
    ret_dic["width"] = width
    ret_dic["samples"] = samples
    ret_dic["interp"] = interp
    ret_dic["central"] = central
    ret_dic["linear"] = linear
    ret_dic["planar"] = planar
    
    return ret_dic

    
                
            
    
    
