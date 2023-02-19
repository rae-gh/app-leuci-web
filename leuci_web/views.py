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

def destinations(request):
    all_destinations = []
    all_cruises = []
    return render(request, 'destinations.html',{'destinations':all_destinations,'cruises':all_cruises})

###################################################################
### Testing for demo broken links ###
def broken(request):
    return render(request,'brokens.html')

@csrf_exempt
def broken0(request):
    return rachelPlot(request)

####################################################################
@csrf_exempt
def plotly(request):
    # https://albertrtk.github.io/2021/01/24/Graph-on-a-web-page-with-Plotly-and-Django.html
    """
    View demonstrating how to display a graph object
    on a web page with Plotly.
    """
    from django.shortcuts import render
    from plotly.offline import plot
    import plotly.graph_objects as go
    # Generating some data for plots.
    x = [i for i in range(-10, 11)]
    y1 = [3*i for i in x]
    y2 = [i**2 for i in x]
    y3 = [10*abs(i) for i in x]
    # List of graph objects for figure.
    # Each object will contain on series of data.
    graphs = []
    # Adding linear plot of y1 vs. x.
    graphs.append(
        go.Scatter(x=x, y=y1, mode='lines', name='Line y1')
    )
    # Adding scatter plot of y2 vs. x.
    # Size of markers defined by y2 value.
    graphs.append(
        go.Scatter(x=x, y=y2, mode='markers', opacity=0.8,
        marker_size=y2, name='Scatter y2')
    )
    # Adding bar plot of y3 vs x.
    graphs.append(
        go.Bar(x=x, y=y3, name='Bar y3')
    )
    # Setting layout of the figure.
    layout = {
        'title': 'Title of the figure',
        'xaxis_title': 'X',
        'yaxis_title': 'Y',
        'height': 420,
        'width': 560,
    }
    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, output_type='div')
    return render(request, 'plotly.html',context={'plot_div': plot_div})

@csrf_exempt
def matplotlib(request):    
    import matplotlib.pyplot as plt
    import io
    import base64    
    name = request.POST.get('name')     
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])    
    flike = io.BytesIO()
    plt.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()    
    context = {'wind_rose': b64,'name': name }            
    return render(request, 'matplotlib.html', context)
    
### Brokens  ############################################################
@csrf_exempt
def rachelPlot(request):    
    import matplotlib.pyplot as plt
    import io
    import base64    
    if 'name' in request.POST:
        name = request.POST.get('name')     
    else:
        name=""
    fig, ax = plt.subplots(figsize=(5,2))    
    data = pd.read_csv("leuci_web/static/res/data/notch1_3l95_ddg_background.csv")
    x = data['pdb_rid']
    y = data['ddg']
    ax.plot(x,y)   
    flike = io.BytesIO()
    plt.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()    
    context = {'wind_rose': b64,'name': name }            
    return render(request, 'broken0.html', context)


@csrf_exempt
def density_fetch(request):
    
    pdb_code, resolution, ebi_link,exp_method,map_header = sd.get_pdbcode(request)            
    context = {
        'pdb_code': pdb_code, 
        'resolution':resolution, 
        'ebi_link':ebi_link,
        'exp_method':exp_method,
        'map_header':map_header,
         }            
    return render(request, 'explore.html', context)


# ASYNC STUFF ############################################################################################
# helpers
async def http_call_async():
    for num in range(1, 6):
        await asyncio.sleep(1)
        print(num)
    async with httpx.AsyncClient() as client:
        r = await client.get("https://httpbin.org/")
        print(r)


def http_call_sync():
    for num in range(1, 6):
        sleep(1)
        print(num)
    r = httpx.get("https://httpbin.org/")
    print(r)




async def get_smokables():
    print("Getting smokeables...")

    await asyncio.sleep(2)
    async with httpx.AsyncClient() as client:
        await client.get("https://httpbin.org/")

        print("Returning smokeable")
        return [
            "ribs",
            "brisket",
            "lemon chicken",
            "salmon",
            "bison sirloin",
            "sausage",
        ]


async def get_flavor():
    print("Getting flavor...")

    await asyncio.sleep(1)
    async with httpx.AsyncClient() as client:
        await client.get("https://httpbin.org/")

        print("Returning flavor")
        return random.choice(
            [
                "Sweet Baby Ray's",
                "Stubb's Original",
                "Famous Dave's",
            ]
        )


def oversmoke() -> None:
    """ If it's not dry, it must be uncooked """
    sleep(5)
    print("Who doesn't love burnt meats?")

# views
async def async_view(request):
    loop = asyncio.get_event_loop()
    loop.create_task(http_call_async())
    return HttpResponse("Non-blocking HTTP request")


def sync_view(request):
    http_call_sync()
    return HttpResponse("Blocking HTTP request")


async def smoke(smokables: List[str] = None, flavor: str = "Sweet Baby Ray's") -> List[str]:
    """ Smokes some meats and applies the Sweet Baby Ray's """

    for smokable in smokables:
        print(f"Smoking some {smokable}...")
        print(f"Applying the {flavor}...")
        print(f"{smokable.capitalize()} smoked.")

    return len(smokables)

async def smoke_some_meats(request):
    results = await asyncio.gather(*[get_smokables(), get_flavor()])
    total = await asyncio.gather(*[smoke(results[0], results[1])])
    return HttpResponse(f"Smoked {total[0]} meats with {results[1]}!")


async def burn_some_meats(request):
    oversmoke()
    return HttpResponse(f"Burned some meats.")


async def async_with_sync_view(request):
    loop = asyncio.get_event_loop()
    async_function = sync_to_async(http_call_sync, thread_sensitive=False)
    loop.create_task(async_function())
    return HttpResponse("Non-blocking HTTP request (via sync_to_async)")

#####################################################################################################################################

from pathlib import Path
import datetime    
import logging 
from django.http import JsonResponse
from asgiref.sync import async_to_sync, sync_to_async

DIR = str(Path(__file__).resolve().parent )+ "/data/"

def download_ed(pdbcode):    
    from leuci_lib import pdbobject as pob
    my_pdb = pob.PdbObject(pdbcode, directory=DIR)
    my_pdb.download()    
    #import urllib.request
    #urllib.request.urlretrieve(f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdbcode}.ent", filename)

gl_user = ""
gl_ip = ""

@sync_to_async
def get_user(request):
    gl_user = request.user.id    
    #gl_ip = request.META['REMOTE_ADDR']
    #from ipware import get_client_ip
    gl_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
    #gl_ip, is_routable = get_client_ip(request)
    
        
async def explore(request):
    context = {
        'pdb_code': "", 
        'resolution':"", 
        'ebi_link':"",
        'exp_method':"",
        'map_header':{},
        'message':""
         }

    pdb_code = "6eex"
    if 'pdb_code' in request.POST:
        pdb_code = request.POST.get('pdb_code')
    get_user(request)
    
    from leuci_lib import pdbobject as pob
    my_pdb = pob.PdbObject(pdb_code,directory=DIR)
    context['pdb_code'] = pdb_code        
    logging.info("INFO:\t" + gl_user + "\t" + gl_ip + "\t" + pdb_code + ' was explored at '+str(datetime.datetime.now())+' hours')
    if my_pdb.exists():
        context['resolution'] = my_pdb.resolution
        context['ebi_link'] = my_pdb.ebi_link
        context['exp_method'] = my_pdb.exp_method
        my_pdb.load()
        if my_pdb.em_loaded:
            context['map_header'] = my_pdb.map_header
            context['header_string'] = my_pdb.header_as_string
        return render(request, 'explore.html', context)
        
    else:        
        context['ebi_link'] = my_pdb.ebi_link
        context['message'] = "Downloading... "        
        loop = asyncio.get_event_loop()
        async_function = sync_to_async(download_ed, thread_sensitive=False)
        loop.create_task(async_function(pdb_code))                
        return render(request, 'explore.html', context)

@csrf_exempt
def admin(request):
    act = ""
    if 'act' in request.POST:
        act = request.POST.get('act')
    
    context = {}    
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

                        
    return render(request, 'admin.html', context)
        