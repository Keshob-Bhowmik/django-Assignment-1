from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from event.forms import EventModelForm, CreateCategoryModelForm, AddParticepantModelform
from event.models import Event, Participant, Category
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Prefetch
# Create your views here.
@login_required
def Dashboard(request):
    type=request.GET.get('type')
    return render(request, 'admin/admin_dashboard.html', {'type':type})



def Home(request):
    events = Event.objects.select_related('category').prefetch_related('particepant').all()
    context={
        'events' : events
    }
    return render(request, 'dashboard/home.html', context)
@login_required
def Past_events(request):
    return render(request, 'dashboard/past-events.html')

@login_required
def details(request, id):
    event = Event.objects.prefetch_related('particepant').get(id=id)
    
    context = {
        'event' : event
    }
    return render(request, 'dashboard/event_details.html', context)


def All_events(request): 
    type = request.GET.get('type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    print(start_date)
    print(end_date)
    

    print(type)
    today = timezone.now().date()
    counts = Event.objects.aggregate(
        total_events = Count('id', distinct=True),
        upcoming_events = Count('id', filter=Q(date__gt=today), distinct=True),
        past_events = Count('id', filter=Q(date__lt=today), distinct=True),
        total_particepant = Count('particepant', distinct=True)
    )
    events = Event.objects.select_related('category').prefetch_related('particepant').all()
    if start_date and end_date:
        if start_date<=end_date:
            events = events.filter(date__range=(start_date,end_date))
            if events.exists():
                type='date'
            else:
                type='date-no-events'
                # events = events.none()
            
        elif start_date>end_date:
            type='wrong-date'
            events = events.none()
    elif start_date=="" or end_date=="":
        type = "empty-date"
        events=events.none()
    elif type=='upcoming':
        events = events.filter(date__gt=today)
    elif type=='past':
        events=events.filter(date__lt=today)
    elif type=='total-event':
        pass
    else:
        events=events.filter(date=today)
    context = {
        'events': events,
        'type' : type,
        'counts' : counts,
        'start_date' : start_date,
        'end_date' : end_date
    }
    print(type)
    return render(request, 'dashboard/events.html', context)


@login_required
def searchBynameLocation(request):
    search_key = request.GET.get('key')
    print(search_key)
    if search_key:
        events = Event.objects.filter(
            Q(name__icontains=search_key) | Q(location__icontains=search_key)
        ).select_related('category').prefetch_related('particepant')
    else:
        events = Event.objects.none()

    context = {
        'search_key' : search_key,
        'events' : events
    }
    return render(request, 'dashboard/searchByNameLocation.html', context)



@login_required
def Categories(request):
    type= request.GET.get('type')
    categories = Category.objects.all()
    context = {
        'type' : type,
        'categories' : categories
    }
    return render(request, 'dashboard/category.html',context)

@login_required
def categories_events(request, id):

    events = Event.objects.filter(category_id=id).select_related('category')
    context={
        'events' : events
    }
    return render(request, 'dashboard/category_events.html', context)


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventModelForm(request.POST)
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
def remove_event(request):
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        if event_id:
            event = Event.objects.get(id=event_id)
            event.delete()
            Participant.objects.annotate(event_count=Count('events')).filter(event_count=0).delete()
            messages.success(request, "The Event is deleted successfully")
            return redirect('remove_event')
    search_key = request.GET.get('key')
    event_ache = None
    print(search_key)
    if 'key' in request.GET:
        if search_key:
            events = Event.objects.filter(
                Q(name__icontains=search_key) | Q(location__icontains=search_key)
            ).select_related('category').prefetch_related('particepant')
            if not events:
                event_ache = 'no'
        else:
            events = Event.objects.none()
            event_ache='empty_search'
    else:
        events = Event.objects.none()

    context = {
        'search_key' : search_key,
        'events' : events,
        'event_ache' : event_ache
    }
    return render(request, 'dashboard/remove-event.html', context)



@login_required
def update_event(request):
    event = None
    form = None

    
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        if event_id:
            event = Event.objects.get(id=event_id)
            form = EventModelForm(request.POST, instance=event)
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
            ).select_related('category').prefetch_related('particepant')
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
    return render(request, 'dashboard/update-event.html', context)




@login_required
def remove_particepant(request):

    if request.method == "POST":
        particepant_id = request.POST.get('particepant_id')
        if particepant_id:
            particepant = Participant.objects.get(id=particepant_id)
            particepant.delete()
            messages.success(request, "Particepant Removed Successfully")
            return redirect('removeparticepant')

    search_key = request.GET.get('key')
    particepant_ache = None
    if 'key' in request.GET:
        if search_key:
            particepants = Participant.objects.filter(name__icontains=search_key)
            if not particepants:
                particepant_ache = 'no'
        else:
            particepants = Participant.objects.none()
            particepant_ache = 'empty_search'
    else:
        particepants = Participant.objects.none()
    context={
        'particepants' : particepants,
        'search_key' : search_key,
        'particepant_ache' : particepant_ache
    }
    return render(request, 'dashboard/remove-particepant.html', context)



@login_required
def update_particepant(request):
    particepant = None
    form = None
    if request.method == "POST":
        particepant_id = request.POST.get('particepant_id')
        if particepant_id:
            particepant = Participant.objects.get(id=particepant_id)
            form = AddParticepantModelform(request.POST, instance=particepant)
            if form.is_valid():
                form.save()
                messages.success(request, "Particepant Updated Successfully")
                return redirect('updateparticepant')
    search_key = request.GET.get('key')
    edit_id = request.GET.get('edit_id')
    particepant_ache = None
    edit_id_ache = None
    if 'key' in request.GET:
        if search_key:
            particepants = Participant.objects.filter(name__icontains=search_key)
            if not particepants:
                particepant_ache = 'no'
        else:
            particepants = Participant.objects.none()
            particepant_ache = 'empty_search'
    else:
        particepants = Participant.objects.none()
    if edit_id:
        particepant = Participant.objects.get(id=edit_id)
        form = AddParticepantModelform(instance=particepant)
        edit_id_ache = 'yes'

    context={
        'search_key' : search_key,
        'particepant_ache' : particepant_ache,
        'edit_id_ache' : edit_id_ache,
        'particepants' : particepants,
        'form' : form,
        'edit_particepant' : particepant
    }
    return render(request, 'dashboard/update-particepant.html', context)




@login_required
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
def addparticepant(request):
    form = AddParticepantModelform()
    if request.method == 'POST':
        form = AddParticepantModelform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Particepant Added Successfully")
            return redirect('addparticepant')
            
    context = {
        'form' : form
    }
    return render(request, 'dashboard/add-particepant.html', context)



