"""
RSA - 3rd Feb 2023
This file returns info that the user has in scope during the session anonymously

"""
#from leuci_lib import pdbobject as pob
import datetime    
import logging        
from pathlib import Path
from asgiref.sync import async_to_sync, sync_to_async
import json

DIR = str(Path(__file__).resolve().parent )+ "/data/"

import leuci_lib.mapobject as mobj
import leuci_lib.maploader as moad

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
def get_pdbcode(request):
    """
    Returns pdb info from current state or downloads from the ebi
    """
    pdb_code,in_store, exists,ready_header,mload = "", False,False,False,None    
    current_code = ""
    if 'pdb_code' in request.POST:
        pdb_code = request.POST.get('pdb_code').lower()        
    elif 'pdb_code' in request.GET:
        pdb_code = request.GET.get('pdb_code').lower()        
    if 'pdb_code' in request.session:
        current_code = request.session['pdb_code'].lower()            
        if pdb_code == "":
            pdb_code = current_code    
    if current_code == pdb_code:
        ready_header = True            
    mload = moad.MapLoader(pdb_code, directory=DIR, cif=False)        
    stre = stor.Store()
    if stre.exists(pdb_code):
        mobj,dt = stre.get(pdb_code)
        mload.mobj = mobj
        in_store = True            
    #return pdb_code, in_store,exists, ready_header, mload
    request.session['pdb_code'] = pdb_code    
    exists = mload.exists()
    return pdb_code, in_store,exists, ready_header, mload
   
@sync_to_async
def load_mapheader(request,pdb_code,mload):        
    if not mload.exists():
        mload.download()    
    mload.load()
    mob = mload.mobj
    #mob_json = json.dumps(mob.toJson(), indent=4)        
    #key = pdb_code + "_data"    
    #request.session[key] = mob_json
    request.session["pdb_code"] = pdb_code
    return mload


def download_ed(request,pdb_code,gl_ip):    
    print("downloading...")
    from leuci_lib import maploader as mob
    my_pdb = mob.MapLoader(pdb_code, directory=DIR)
    my_pdb.download()
    logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' was downloaded at '+str(datetime.datetime.now())+' hours')
    upload_ed(request,pdb_code,gl_ip)
    #import urllib.request
    #urllib.request.urlretrieve(f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdbcode}.ent", filename)

def upload_ed(request,pdb_code,gl_ip):
    print("uploading...")
    from leuci_lib import maploader as mob
    import json
    mload = mob.MapLoader(pdb_code, directory=DIR)
    mload.load()
    mload.load_values()           
    mload.load_values(diff=True)    

    stre = stor.Store()
    if not stre.exists(pdb_code):
        stre.add(pdb_code,mload.mobj)
        print("added",pdb_code,"to store")
        
    #mob = mload.mobj    
    #mob_json = json.dumps(mob.toJson(), indent=4)        
    #key1 = pdbcode + "_data"    
    #key2 = pdbcode + "_values" 
    #request.session[key1] = mob_json
    #request.session[key2] = "Y"    
    logging.info("INFO:\t" + gl_ip + "\t" + pdb_code + ' was uploaded at '+str(datetime.datetime.now())+' hours')

def get_store_info(gl_ip):
    from leuci_lib import maploader as mob    
    ret_text = ""
    stre = stor.Store()
    st_dts = stre.storage_dates()
    for pdb_code,map_obj in stre.storage().items():        
        ret_text += "\n" + pdb_code + "\t" + map_obj.header_as_string[:30] + "\n"                    
        if len(map_obj.values) > 0:
            dt = st_dts[pdb_code]
            ret_text += "vals=" + str(len(map_obj.values)) + "\t\t"
            ret_text += str(dt) + "\n"

    #mob = mload.mobj    
    #mob_json = json.dumps(mob.toJson(), indent=4)        
    #key1 = pdbcode + "_data"    
    #key2 = pdbcode + "_values" 
    #request.session[key1] = mob_json
    #request.session[key2] = "Y"    
    logging.info("INFO:\t" + gl_ip + "\t" + ' store viewed at '+str(datetime.datetime.now())+' hours')
    return ret_text