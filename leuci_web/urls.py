## APP (Leuci-Web)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),                
    path('explore', views.explore, name='explore'),
    path('projection', views.projection, name='projection'),
    path('slice', views.slice, name='slice'),
    path('slice_settings', views.slice_settings, name='slice_settings'),
    path('admin', views.admin, name='admin'),
                    
]