from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('new_search',views.search,name='new_search'),
    ]