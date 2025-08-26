from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from event.forms import EventModelForm, CreateCategoryModelForm, AssignRoleForm, CreateGroupForm
from event.models import Event, Category
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import User, Group
from django.db.models import Prefetch
# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_particepant(user):
    return user.groups.filter(name='Particepant').exists()




@login_required
@user_passes_test(is_admin)
def Dashboard(request):
    type = request.GET.get('type')
    return render(request, 'dashboard/dashboard.html', {'type' : type})



def Home(request):
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    source = request.GET.get('source', 'home')
    context = {
        'events': events,
        'source' : source
    }
    return render(request, 'dashboard/home.html', context)




def Past_events(request):
    return render(request, 'dashboard/past-events.html')

@login_required
def details(request, id):
    event = Event.objects.prefetch_related('participants').get(id=id)
    source = request.GET.get('source', 'all')
    
    context = {
        'event': event,
        'source' : source
    }
    return render(request, 'dashboard/event_details.html', context)


def All_events(request): 
    type = request.GET.get('type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    today = timezone.now().date()
    counts = Event.objects.aggregate(
        total_events = Count('id', distinct=True),
        upcoming_events = Count('id', filter=Q(date__gt=today), distinct=True),
        past_events = Count('id', filter=Q(date__lt=today), distinct=True),
        total_participants = Count('participants', distinct=True)  # updated here
    )
    
    events = Event.objects.select_related('category').prefetch_related('participants').all()  # updated here
    
    if start_date and end_date:
        if start_date <= end_date:
            events = events.filter(date__range=(start_date, end_date))
            type = 'date' if events.exists() else 'date-no-events'
        else:
            type = 'wrong-date'
            events = events.none()
    elif start_date == "" or end_date == "":
        type = "empty-date"
        events = events.none()
    elif type == 'upcoming':
        events = events.filter(date__gt=today)
    elif type == 'past':
        events = events.filter(date__lt=today)
    elif type == 'total-event':
        pass
    else:
        events = events.filter(date=today)
    
    context = {
        'events': events,
        'type': type,
        'counts': counts,
        'start_date': start_date,
        'end_date': end_date
    }
    
    return render(request, 'dashboard/events.html', context)




def searchBynameLocation(request):
    search_key = request.GET.get('key')
    print(search_key)
    if search_key:
        events = Event.objects.filter(
            Q(name__icontains=search_key) | Q(location__icontains=search_key)
        ).select_related('category').prefetch_related('participants')  # updated here
    else:
        events = Event.objects.none()

    context = {
        'search_key': search_key,
        'events': events
    }
    return render(request, 'dashboard/searchByNameLocation.html', context)





def Categories(request):
    type= request.GET.get('type')
    categories = Category.objects.all()
    context = {
        'type' : type,
        'categories' : categories
    }
    return render(request, 'dashboard/category.html',context)


def categories_events(request, id):

    events = Event.objects.filter(category_id=id).select_related('category')
    context={
        'events' : events
    }
    return render(request, 'dashboard/category_events.html', context)


@login_required
@permission_required('event.add_event')
def create_event(request):
    if request.method == 'POST':
        form = EventModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('create-event')
    else:
        form = EventModelForm()
    context = {
        'form' : form,

    }
    return render(request, 'dashboard/create-event-form.html', context)



@login_required
@permission_required('event.delete_event')
def remove_event(request):
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        if event_id:
            event = Event.objects.get(id=event_id)
            event.delete()
            messages.success(request, "The Event is deleted successfully")
            return redirect('remove_event')

    search_key = request.GET.get('key')
    event_ache = None
    if 'key' in request.GET:
        if search_key:
            events = Event.objects.filter(
                Q(name__icontains=search_key) | Q(location__icontains=search_key)
            ).select_related('category').prefetch_related('participants')
            if not events:
                event_ache = 'no'
        else:
            events = Event.objects.none()
            event_ache = 'empty_search'
    else:
        events = Event.objects.none()

    context = {
        'search_key': search_key,
        'events': events,
        'event_ache': event_ache
    }
    return render(request, 'dashboard/remove-event.html', context)




@login_required
@permission_required('event.change_event')
def update_event(request):
    event = None
    form = None

    if request.method == "POST":
        event_id = request.POST.get('event_id')
        if event_id:
            event = Event.objects.get(id=event_id)
            form = EventModelForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request, "Event updated successfully.")
                return redirect('update_event')

    search_key = request.GET.get('key')
    edit_id = request.GET.get('edit_id')
    event_ache = None
    edit_id_ache = None
    if 'key' in request.GET:
        if search_key:
            events = Event.objects.filter(
                Q(name__icontains=search_key) | Q(location__icontains=search_key)
            ).select_related('category').prefetch_related('participants')
            if not events:
                event_ache = 'no'
        else:
            events = Event.objects.none()
            event_ache = 'empty_search'
    else:
        events = Event.objects.none()

    if edit_id:
        event = Event.objects.get(id=edit_id)
        form = EventModelForm(instance=event)
        edit_id_ache = 'yes'

    context = {
        'search_key': search_key,
        'events': events,
        'event_ache': event_ache,
        'edit_event': event,
        'form': form,
        'edit_id_ache': edit_id_ache
    }
    return render(request, 'dashboard/update-event.html', context)





@login_required
@permission_required('auth.delete_user', raise_exception=True)
def remove_particepant(request):
    participant_group = Group.objects.get(name="Particepant")  

    if request.method == "POST":
        user_id = request.POST.get('particepant_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id, groups=participant_group)
                user.delete()
                messages.success(request, "Participant removed successfully")
            except User.DoesNotExist:
                messages.error(request, "Participant not found")
            return redirect('removeparticepant')

    search_key = request.GET.get('key')
    particepant_ache = None

    if search_key is not None:
        if search_key.strip() != "":
            particepants = User.objects.filter(
                groups=participant_group,
                username__icontains=search_key
            )
            if not particepants.exists():
                particepant_ache = 'no'
        else:
            particepants = User.objects.none()
            particepant_ache = 'empty_search'
    else:
        particepants = None 

    context = {
        'particepants': particepants,
        'search_key': search_key,
        'particepant_ache': particepant_ache
    }

    return render(request, 'dashboard/remove-particepant.html', context)



@login_required
@permission_required('auth.change_user')  
def update_particepant(request):
    particepant = None
    search_key = request.GET.get('key')
    edit_id = request.GET.get('edit_id')
    particepant_ache = None
    edit_id_ache = None
    particepants = User.objects.none()  

    if 'key' in request.GET:
        if search_key:
            particepants = User.objects.filter(
                username__icontains=search_key,
                groups__name="Particepant"
            )
            if not particepants.exists():
                particepant_ache = 'no'
        else:
            particepants = User.objects.none()
            particepant_ache = 'empty_search'

    
    if edit_id:
        particepant = get_object_or_404(
            User, 
            id=edit_id, 
            groups__name="Particepant" 
        )
        edit_id_ache = 'yes'

 
    if request.method == "POST":
        particepant_id = request.POST.get('particepant_id')
        if particepant_id:
            particepant = get_object_or_404(
                User, 
                id=particepant_id, 
                groups__name="Particepant" 
            )
            username = request.POST.get('username')
            email = request.POST.get('email')
            if username and email:
                particepant.username = username
                particepant.email = email
                particepant.save()
                messages.success(request, "Participant updated successfully.")
                return redirect('updateparticepant')

    context = {
        'search_key': search_key,
        'particepant_ache': particepant_ache,
        'edit_id_ache': edit_id_ache,
        'particepants': particepants,
        'edit_particepant': particepant
    }
    return render(request, 'dashboard/update-particepant.html', context)





@login_required
@permission_required('event.add_category')
def create_category(request):
    form = CreateCategoryModelForm()
    if request.method == 'POST':
        form = CreateCategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Added Successfully")
            return redirect('create-category')
        
    context = {
        'form' : form
    }
    return render(request, 'dashboard/create-category-form.html', context)




@login_required
@permission_required('event.delete_category')
def remove_category(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        if category_id:
            category = Category.objects.get(id=category_id)
            category.delete()
            messages.success(request, "Category Removed Successfully")
            return redirect('removecategory')

    search_key = request.GET.get('key')
    category_ache = None
    if 'key' in request.GET:
        if search_key:
            categories = Category.objects.filter(name__icontains=search_key)
            if not categories:
                category_ache = 'no'
        else:
            categories = Category.objects.none()
            category_ache = 'empty_search'
    else:
        categories = Category.objects.none()
    context={
        'categories' : categories,
        'search_key' : search_key,
        'category_ache' : category_ache
    }
    return render(request, 'dashboard/remove-category.html', context)



@login_required
@permission_required('event.change_category')
def update_category(request):
    category = None
    form = None
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        if category_id:
            category = Category.objects.get(id=category_id)
            form = CreateCategoryModelForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, "Category Updated Successfully")
                return redirect('updatecategory')
    search_key = request.GET.get('key')
    edit_id = request.GET.get('edit_id')
    category_ache = None
    edit_id_ache = None
    if 'key' in request.GET:
        if search_key:
            categories = Category.objects.filter(name__icontains=search_key)
            if not categories:
                category_ache = 'no'
        else:
            categories = Category.objects.none()
            category_ache = 'empty_search'
    else:
        categories = Category.objects.none()
    if edit_id:
        category = Category.objects.get(id=edit_id)
        form = CreateCategoryModelForm(instance=category)
        edit_id_ache = 'yes'

    context={
        'search_key' : search_key,
        'category_ache' : category_ache,
        'edit_id_ache' : edit_id_ache,
        'categories' : categories,
        'form' : form,
        'edit_category' : category
    }
    return render(request, 'dashboard/update-category.html', context)




@login_required
@user_passes_test(is_admin)
def all_participants(request):
    participants = User.objects.filter(groups__name='Particepant')

    context = {
        'participants': participants,
    }
    return render(request, 'dashboard/all-participants.html', context)



#admin part
@login_required
@permission_required('auth.view_user')
def user_list(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    # print(users)

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'dashboard/user_list.html', {"users": users})


@login_required
@user_passes_test(is_admin)
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to role {role.name}")
            return redirect('user_list')
    return render(request, 'dashboard/assign_role.html', {'form' : form})
@login_required
@permission_required('auth.add_group')
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} is created successfully.")
            return redirect('create_group')
    return render(request, 'dashboard/create_group.html', {'form' : form})

@login_required
@permission_required('auth.view_group')
def show_group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'dashboard/show_group_list.html', {'groups' : groups})

@login_required
@permission_required('auth.delete_group')
def delete_group(request, group_id):
    if request.method == 'POST':
        group = Group.objects.get(id=group_id)
        group_name = group.name
        group.delete()
        messages.success(request, f"Group {group_name} is deleted successfully")
    return redirect('show_group_list')



#organizer part

@login_required
@user_passes_test(is_organizer)
def organizer_dashboard(request):
    type = request.GET.get('type')
    context = {
        'type': type,
    }
    return render(request, 'organizer/organizer_dashboard.html', context)



@login_required
@permission_required('event.add_event')
def organizer_create_event(request):
    if request.method == 'POST':
        form = EventModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('organizer_create_event')
    else:
        form = EventModelForm()
    context = {
        'form' : form,

    }
    return render(request, 'organizer/org-create-event-form.html', context)



@login_required
@permission_required('event.delete_event')
def organizer_remove_event(request):
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        if event_id:
            event = Event.objects.get(id=event_id)
            event.delete()
            messages.success(request, "The Event is deleted successfully")
            return redirect('organizer_remove_event')

    search_key = request.GET.get('key')
    event_ache = None
    if 'key' in request.GET:
        if search_key:
            events = Event.objects.filter(
                Q(name__icontains=search_key) | Q(location__icontains=search_key)
            ).select_related('category').prefetch_related('participants')
            if not events:
                event_ache = 'no'
        else:
            events = Event.objects.none()
            event_ache='empty_search'
    else:
        events = Event.objects.none()

    context = {
        'search_key': search_key,
        'events': events,
        'event_ache': event_ache
    }
    return render(request, 'organizer/org-remove-event.html', context)



@login_required
@permission_required('event.change_event')
def organizer_update_event(request):
    event = None
    form = None

    
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        if event_id:
            event = Event.objects.get(id=event_id)
            form = EventModelForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request, "Event updated successfully.")
                return redirect('organizer_update_event')

   
    search_key = request.GET.get('key')
    edit_id = request.GET.get('edit_id')
    event_ache = None
    edit_id_ache = None
    if 'key' in request.GET:
        if search_key:
            events = Event.objects.filter(
                Q(name__icontains=search_key) | Q(location__icontains=search_key)
            ).select_related('category').prefetch_related('participants')
            if not events:
                event_ache = 'no'
        else:
            events = Event.objects.none()
            event_ache = 'empty_search'
    else:
        events = Event.objects.none()

    if edit_id:
        event = Event.objects.get(id=edit_id)
        form = EventModelForm(instance=event)
        edit_id_ache = 'yes'
    print(edit_id_ache)
    context = {
        'search_key': search_key,
        'events': events,
        'event_ache': event_ache,
        'edit_event': event,
        'form': form,
        'edit_id_ache' : edit_id_ache
    }
    return render(request, 'organizer/org-update-event.html', context)



@login_required
@permission_required('event.add_category')
def organizer_create_category(request):
    form = CreateCategoryModelForm()
    if request.method == 'POST':
        form = CreateCategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Added Successfully")
            return redirect('organizer_create_category')
        
    context = {
        'form' : form
    }
    return render(request, 'organizer/org-create-category.html', context)


@login_required
@permission_required('event.delete_category')
def organizer_remove_category(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        if category_id:
            category = Category.objects.get(id=category_id)
            category.delete()
            messages.success(request, "Category Removed Successfully")
            return redirect('organizer_remove_category')

    search_key = request.GET.get('key')
    category_ache = None
    if 'key' in request.GET:
        if search_key:
            categories = Category.objects.filter(name__icontains=search_key)
            if not categories:
                category_ache = 'no'
        else:
            categories = Category.objects.none()
            category_ache = 'empty_search'
    else:
        categories = Category.objects.none()
    context={
        'categories' : categories,
        'search_key' : search_key,
        'category_ache' : category_ache
    }
    return render(request, 'organizer/org-remove-category.html', context)


@login_required
@permission_required('event.change_category')

def oranizer_update_category(request):
    category = None
    form = None
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        if category_id:
            category = Category.objects.get(id=category_id)
            form = CreateCategoryModelForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, "Category Updated Successfully")
                return redirect('oranizer_update_category')
    search_key = request.GET.get('key')
    edit_id = request.GET.get('edit_id')
    category_ache = None
    edit_id_ache = None
    if 'key' in request.GET:
        if search_key:
            categories = Category.objects.filter(name__icontains=search_key)
            if not categories:
                category_ache = 'no'
        else:
            categories = Category.objects.none()
            category_ache = 'empty_search'
    else:
        categories = Category.objects.none()
    if edit_id:
        category = Category.objects.get(id=edit_id)
        form = CreateCategoryModelForm(instance=category)
        edit_id_ache = 'yes'

    context={
        'search_key' : search_key,
        'category_ache' : category_ache,
        'edit_id_ache' : edit_id_ache,
        'categories' : categories,
        'form' : form,
        'edit_category' : category
    }
    return render(request, 'organizer/org-update-category.html', context)



#participants part
@login_required
@permission_required('event.view_event')
def participants_dashboard(request):
    type = request.GET.get('type')
    context = {
        'type': type,
    }
    return render(request, 'participant/participant_dashboard.html', context)

@login_required
@user_passes_test(is_particepant)
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    if user in event.participants.all():
        messages.warning(request, f"You have already RSVPed to this event {event.name}.")
    else:
        event.participants.add(user)
        messages.success(request, "Successfully RSVPed to the event!")
    return redirect('participants_dashboard')

@login_required
@user_passes_test(is_particepant)
def view_rsvp_events(request):
    rsvpd_events = Event.objects.filter(participants=request.user)
    source = request.GET.get('source', 'view_rsvp_events')
    context = {
        'rsvpd_events' : rsvpd_events,
        'source' : source
    }
    return render(request, 'participant/rsvp_events.html', context)