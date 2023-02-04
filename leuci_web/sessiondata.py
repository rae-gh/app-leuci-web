"""
RSA - 3rd Feb 2023
This file returns info that the user has in scope during the session anonymously

"""
from leuci_lib import pdbobject as pob

def get_pdbcode(request):
    """
    Returns pdb info from current state or downloads from the ebi


    """
    new_pdb_code = "6eex"
    if 'pdb_code' in request.POST:
        new_pdb_code = request.POST.get('pdb_code')

    now_pdb_code = ""
    if 'pdb_code' in request.session:
        now_pdb_code = request.session['pdb_code']

    if now_pdb_code != new_pdb_code:            
        po = pob.PdbObject(new_pdb_code)
        if po.valid:
            request.session['pdb_code'] = new_pdb_code
            request.session['resolution'] = po.resolution
            request.session['ebi_link'] = po.ebi_link
        else:
            request.session['pdb_code'] = "invalid"
            request.session['resolution'] = -1
            request.session['ebi_link'] = ""

    return request.session['pdb_code'], request.session['resolution'],request.session['ebi_link']