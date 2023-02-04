## APP (Leuci-Web)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),                
    path('explore', views.explore, name='explore'),
    path('plotly', views.plotly, name='plotly'),
    path('matplotlib', views.matplotlib, name='matplotlib'),  
    
]