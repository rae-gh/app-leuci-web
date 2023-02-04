from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages.views import SuccessMessageMixin
import plotly.graph_objects as go
import pandas as pd

# my files
from . import sessiondata as sd

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
    

class DestinationDetailView(generic.DetailView):        
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'

class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'    
    model = models.Cruise
    context_object_name = 'cruise'

class InfoRequestCreate(SuccessMessageMixin,generic.CreateView):
    template_name = 'info_request_complete.html'
    model = models.InfoRequest
    fields = ['name','email','cruise','notes']
    success_url=reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more info about &(cruise)s'

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
def explore(request):    
    pdb_code, resolution, ebi_link = sd.get_pdbcode(request)
    context = {'pdb_code': pdb_code, 'resolution':resolution, 'ebi_link':ebi_link }            
    return render(request, 'explore.html', context)
