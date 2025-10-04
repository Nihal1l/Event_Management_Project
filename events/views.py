from django.contrib import messages
from django.shortcuts import render , redirect
from django.http import HttpResponse
from users.views import is_admin
from .forms import *
from .models import *
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
# Create your views here.

# Create your views here.
def is_participant(user):
    return user.groups.filter(name='Participant').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    type = request.GET.get('type', 'all')

    counts = Event.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING')),
    )

    base_query = Event.objects.select_related(
        'category').prefetch_related('participants').annotate(participants_count=Count('participants'))

    if type == 'completed':
        events = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        events = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        events = base_query.filter(status='PENDING')
    elif type == 'all':
        events = base_query.all()

    context = {
        "events": events,
        "counts": counts
    }
    return render(request, "dashboard/dashboard.html", context)


@user_passes_test(is_organizer, login_url='no-permission')
def organizer_dashboard(request):
    type = request.GET.get('type', 'all')

    counts = Event.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING')),
    )

    base_query = Event.objects.select_related(
        'category').prefetch_related('participants').annotate(participants_count=Count('participants'))

    if type == 'completed':
        events = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        events = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        events = base_query.filter(status='PENDING')
    elif type == 'all':
        events = base_query.all()

    context = {
        "events": events,
        "counts": counts
    }
    return render(request, "dashboard/organizer_dashboard.html", context)

@user_passes_test(is_participant)
def participant_dashboard(request):
    return render(request, "dashboard/participant_dashboard.html")


@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_participant(request.user):
        return redirect('participant-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')

@login_required
@permission_required("events.add_event", login_url='no-permission')
def create_event(request):
    # employees = Employee.objects.all()
    event_form = EventModelForm()  # For GET
    event_detail_form = EventDetailModelForm()

    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        event_detail_form = EventDetailModelForm(request.POST, request.FILES)

        if event_form.is_valid() and event_detail_form.is_valid():

            """ For Model Form Data """
            event = event_form.save()
            event_detail = event_detail_form.save(commit=False)
            event_detail.event = event
            event_detail.save()

            messages.success(request, "Event Created Successfully")
            return redirect('create-event')

    context = {"event_form": event_form, "event_detail_form": event_detail_form}
    return render(request, "event_form.html", context)


@login_required
@permission_required("events.change_event", login_url='no-permission')
def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)  # For GET

    if event.details:
        event_detail_form = EventDetailModelForm(instance=event.details)

    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)
        event_detail_form = EventDetailModelForm(
            request.POST, instance=event.details)

        if event_form.is_valid() and event_detail_form.is_valid():

            """ For Model Form Data """
            event = event_form.save()
            event_detail = event_detail_form.save(commit=False)
            event_detail.event = event
            event_detail.save()

            messages.success(request, "Event Updated Successfully")
            return redirect('update-event', id)

    context = {"event_form": event_form, "event_detail_form": event_detail_form}
    return render(request, "event_form.html", context)

@login_required
@permission_required("events.delete_event", login_url='no-permission')
def delete_event(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(id=event_id)
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return redirect('dynamic')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('dynamic')

@login_required
@permission_required("events.view_event", login_url='no-permission')
def view_event(request):
    events = Event.objects.all()
    return render(request, "show_event.html", {"events": events})

@login_required
@permission_required("events.view_event", login_url='no-permission')
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    status_choices = Event.STATUS_CHOICES

    if request.method == 'POST':
        selected_status = request.POST.get('event_status')
        event.status = selected_status
        event.save()
        return redirect('event-details', event.id)

    return render(request, 'event_details.html', {"event": event, 'status_choices': status_choices})
