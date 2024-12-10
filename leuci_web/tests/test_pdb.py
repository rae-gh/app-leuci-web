import leuci_map.mapfunctions as mfun
from leuci_map import mapsmanager as mapss
from leuci_map import maploader as moad

DIR = "leuci_web/data/"

def test_pdb():
    pdb_code = "6eex"    
    mapss.MapsManager().set_dir(DIR)
    mload = mapss.MapsManager().get_or_create("6eex",file=1,header=1,values=1)
    #po = moad.MapLoader(pdb_code,directory=DIR,cif=False)
    #po.download()
    #po.load()
    #po.load_values()
    #mload = po
    
    mfunc = mfun.MapFunctions(pdb_code,mload.mobj,mload.pobj, "linear") #the default method is linear
        
    
    
    
    

test_pdb()