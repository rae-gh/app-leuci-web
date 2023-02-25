## APP (Leuci-Web)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),                
    path('explore', views.explore, name='explore'),
    path('projection', views.projection, name='projection'),
    path('slice', views.slice, name='slice'),
    path('admin', views.admin, name='admin'),
    
    path('plotly', views.plotly, name='plotly'),
    path('matplotlib', views.matplotlib, name='matplotlib'),  
    
    path('smoke_some_meats', views.smoke_some_meats, name='smoke_some_meats'),  
    path('burn_some_meats', views.burn_some_meats, name='burn_some_meats'),  
    path('sync_to_async', views.async_with_sync_view, name='sync_to_async'),  
    path('async', views.async_view, name='async'),  
    path('sync', views.sync_view, name='sync'),  
    
]