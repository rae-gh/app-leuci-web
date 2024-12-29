
from pathlib import Path
DIR = str(Path(__file__).resolve().parent )+ "/data/"

def explore(pdb_code):
    context = {
        'pdb_code': "", 
        'em_code': "", 
        'resolution':"", 
        'ebi_link':"",
        'em_link':"",
        'exp_method':"",
        'map_header':{},
        'message':""
         }
            
    from maptial.map import pdbobject as pob
    my_pdb = pob.PdbObject(pdb_code)
    context['pdb_code'] = pdb_code            
    if not my_pdb.exists():
        my_pdb.download()
    context['resolution'] = my_pdb.resolution
    context['ebi_link'] = my_pdb.ebi_link
    context['em_link'] = my_pdb.em_link
    context['em_code'] = my_pdb.em_code
    context['exp_method'] = my_pdb.exp_method
    my_pdb.load()
    if my_pdb.em_loaded:
        context['map_header'] = my_pdb.map_header
        context['header_string'] = my_pdb.header_as_string                
    print(context)
##################################
explore("6eex")
        
        
