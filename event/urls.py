from django.contrib import admin
from django.urls import path
from event.views import Dashboard, Home, Past_events, All_events, Categories, create_event, create_category,  details, searchBynameLocation, categories_events, remove_event, remove_particepant, update_event, update_particepant, remove_category, update_category, user_list, assign_role, create_group, show_group_list, delete_group, organizer_dashboard, organizer_create_event, organizer_remove_event, organizer_update_event, organizer_create_category, organizer_remove_category, oranizer_update_category, all_participants, participants_dashboard, rsvp_event, view_rsvp_events
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
    path('remove-particepant/', remove_particepant, name='removeparticepant'),
    path('update-particepant/', update_particepant, name='updateparticepant'),
    path('details/<int:id>/', details, name='Details'),
    path('searchBynameLocation/', searchBynameLocation, name='SearchNameLoc'),
    path('remove-event/', remove_event, name='remove_event'),
    path('update-event/', update_event, name='update_event'),
    path('user_list/', user_list, name='user_list'),
    path('assign_role/<int:user_id>/', assign_role, name='assign_role'),
    path('create-group/', create_group, name='create_group'),
    path('show-group-list/', show_group_list, name = 'show_group_list'),
    path('delete_group/<int:group_id>/', delete_group, name = 'delete_group'),
    path('all-participants/', all_participants, name='all_participants'),
    #organizers urls
    path('organizer-dashboard/', organizer_dashboard, name='organizer_dashboard'),
    path('organizer/create_event/', organizer_create_event, name = "organizer_create_event"),
    path('organizer/remove-event/', organizer_remove_event, name='organizer_remove_event'),
    path('organizer/update-event/', organizer_update_event, name='organizer_update_event'),
    path('organizer/create-category/', organizer_create_category, name='organizer_create_category'),
    path('organizer/remove-category/', organizer_remove_category, name='organizer_remove_category'),
    path('organizer/update-category/', oranizer_update_category, name='oranizer_update_category'),

    #participant part
    path('participant-dashboard/', participants_dashboard, name='participants_dashboard'),
    path('participant_rsvp/<int:event_id>/', rsvp_event, name = 'rsvp_event'),
    path('participant/view_rsvpevents/', view_rsvp_events, name = "view_rsvp_events")
]
