from django.contrib import admin
from django.urls import path
from event.views import Dashboard, Home, Past_events, All_events, Categories, create_event, create_category, addparticepant, details, searchBynameLocation, categories_events, remove_event, remove_particepant, update_event, update_particepant, remove_category, update_category
urlpatterns = [
    path('', Home, name='Home'),
    path('home/', Home, name='Home'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('past/', Past_events),
    path('all/', All_events, name='all'),
    path('category/', Categories, name ='category'),
    path('categories_events/<int:id>/', categories_events, name='categories_events'),
    path('create-event/', create_event, name='create-event'),
    path('create-category/', create_category, name='create-category'),
    path('remove-category/', remove_category, name='removecategory'),
    path('update-category/', update_category, name='updatecategory'),
    path('add-particepant/', addparticepant, name='addparticepant'),
    path('remove-particepant/', remove_particepant, name='removeparticepant'),
    path('update-particepant/', update_particepant, name='updateparticepant'),
    path('details/<int:id>/', details, name='Details'),
    path('searchBynameLocation/', searchBynameLocation, name='SearchNameLoc'),
    path('remove-event/', remove_event, name='remove_event'),
    path('update-event/', update_event, name='update_event')
]
