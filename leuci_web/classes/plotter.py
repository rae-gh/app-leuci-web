
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go



def makeContour(z):    
    minv = min(min(z))
    maxv = max(max(z))
    zero_frac = (0 - minv) / (maxv - minv)
    contours = {"start":minv,"end":maxv,"size":(maxv-minv)/20}        
    line =  {"width": 0.5, "color": 'Gray'}

    if minv < 0:
        cs_scl = [[0, 'DimGray'], [zero_frac, 'AliceBlue'], [zero_frac + 0.01, 'LightBlue'], [zero_frac + 0.2, 'CornflowerBlue'], [0.8, 'Crimson'], [1, 'rgb(100, 0, 0)']];
    else:
        cs_scl = [[0, 'AliceBlue'], [0.01, 'LightBlue'], [0.2, 'CornflowerBlue'], [0.8, 'Crimson'], [1, 'rgb(100, 0, 0)']];                    
    graphs = []
    # Adding linear plot of y1 vs. x.    
    graphs.append(
        go.Contour(z=z,colorscale=cs_scl, contours=contours, line=line )
    )    
    layout = {
        'title': '',
        'xaxis_title': '',
        'yaxis_title': '',
        'height': 400,
        'width': 400,
    }    
    return plot({'data': graphs, 'layout': layout}, output_type='div')
    
def makeHeatmap(z):    
    minv = min(min(z))
    maxv = max(max(z))
    zero_frac = (0 - minv) / (maxv - minv)
    contours = {"start":minv,"end":maxv,"size":(maxv-minv)/20}            
    if minv < 0:
        cs_scl = [[0, 'DimGray'], [zero_frac, 'AliceBlue'], [zero_frac + 0.01, 'LightBlue'], [zero_frac + 0.2, 'CornflowerBlue'], [0.8, 'Crimson'], [1, 'rgb(100, 0, 0)']];
    else:
        cs_scl = [[0, 'AliceBlue'], [0.01, 'LightBlue'], [0.2, 'CornflowerBlue'], [0.8, 'Crimson'], [1, 'rgb(100, 0, 0)']];                    
    graphs = []
    # Adding linear plot of y1 vs. x.
    graphs.append(
        go.Heatmap(z=z,colorscale=cs_scl )
    )        
    layout = {
        'title': '',
        'xaxis_title': '',
        'yaxis_title': '',
        'height': 400,
        'width': 400,
    }    
    return plot({'data': graphs, 'layout': layout}, output_type='div')
    