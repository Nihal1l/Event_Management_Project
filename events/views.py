import token
from django.contrib import messages
from django.shortcuts import render , redirect
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from users.views import is_admin
from .forms import *
from .models import *
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.db.models import Prefetch
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()

def is_participant(user):
    return user.groups.filter(name='Participants').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

"""@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    type = request.GET.get('type', 'all')

    counts = Event.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING'))
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
    return render(request, "dashboard/admin_dashboard.html", context)
"""

admin_dashboard_decorators = [login_required, user_passes_test(is_admin, login_url='no-permission')]
@method_decorator(admin_dashboard_decorators, name='dispatch')
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'dashboard/admin_dashboard.html'
    context_object_name = 'events'
    login_url = 'sign-in'

    def test_func(self):
        return is_admin(self.request.user)

    def get_queryset(self):
        type = self.request.GET.get('type', 'all')

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
        return events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts = Event.objects.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='COMPLETED')),
            in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
            pending=Count('id', filter=Q(status='PENDING'))
        )
        context['counts'] = counts
        return context

organizer_dashboard_decorators = [login_required, user_passes_test(is_organizer, login_url='no-permission')]
@method_decorator(organizer_dashboard_decorators, name='dispatch')
class OrganizerDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'dashboard/organizer_dashboard.html'
    context_object_name = 'events'
    login_url = 'sign-in'

    def test_func(self):
        return is_organizer(self.request.user)

    def get_queryset(self):
        type = self.request.GET.get('type', 'all')

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
        return events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts = Event.objects.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='COMPLETED')),
            in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
            pending=Count('id', filter=Q(status='PENDING'))
        )
        context['counts'] = counts
        return context

participant_dashboard_decorators = [login_required, user_passes_test(is_participant, login_url='no-permission')]
@method_decorator(participant_dashboard_decorators, name='dispatch')
class ParticipantDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'dashboard/participant_dashboard.html'
    context_object_name = 'events'
    login_url = 'sign-in'

    def test_func(self):
        return is_participant(self.request.user)

    def get_queryset(self):
        type = self.request.GET.get('type', 'all')

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
        return events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts = Event.objects.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='COMPLETED')),
            in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
            pending=Count('id', filter=Q(status='PENDING'))
        )
        context['counts'] = counts
        return context
"""@user_passes_test(is_organizer, login_url='no-permission')
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
"""
"""@user_passes_test(is_participant)
def participant_dashboard(request):
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
    return render(request, "dashboard/participant_dashboard.html",context)

"""
@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_participant(request.user):
        return redirect('participant-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')
""""
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

            event = event_form.save()
            event_detail = event_detail_form.save(commit=False)
            event_detail.event = event
            event_detail.save()

            messages.success(request, "Event Created Successfully")
            return redirect('create-event')

    context = {"event_form": event_form, "event_detail_form": event_detail_form}
    return render(request, "event_form.html", context)

"""
create_event_decorators = [login_required, permission_required(
    "events.add_event", login_url='no-permission')]
@method_decorator(create_event_decorators, name='dispatch')
class CreateEvent(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    """ For creating Event """
    permission_required = 'events.add_event'
    login_url = 'sign-in'
    template_name = 'event_form.html'

    """ 
    0. Create Event
    1. LoginRequiredMixin
    2. PermissionRequiredMixin
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_form'] = kwargs.get('event_form', EventModelForm())
        context['event_detail_form'] = kwargs.get(
            'event_detail_form', EventDetailModelForm())
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        event_form = EventModelForm(request.POST)
        event_detail_form = EventDetailModelForm(request.POST, request.FILES)

        if event_form.is_valid() and event_detail_form.is_valid():

            """ For Model Form Data """
            event = event_form.save()
            event_detail = event_detail_form.save(commit=False)
            event_detail.event = event
            event_detail.save()

            messages.success(request, "Event Created Successfully")
            context = self.get_context_data(
                event_form=event_form, event_detail_form=event_detail_form)
            return render(request, self.template_name, context)


update_event_decorators = [login_required, permission_required(
    "events.change_event", login_url='no-permission')]
@method_decorator(update_event_decorators, name='dispatch')
class UpdateEvent(UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = 'event_form.html'
    context_object_name = 'event'
    pk_url_kwarg = 'event_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_form'] = self.get_form()
        # print(context)
        if hasattr(self.object, 'details') and self.object.details:
            context['event_detail_form'] = EventDetailModelForm(
                instance=self.object.details)
        else:
            context['event_detail_form'] = EventDetailModelForm()

        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event_form = EventModelForm(request.POST, instance=self.object)

        event_detail_form = EventDetailModelForm(
            request.POST, request.FILES, instance=getattr(self.object, 'details', None))

        if event_form.is_valid() and event_detail_form.is_valid():

            """ For Model Form Data """
            event = event_form.save()
            event_detail = event_detail_form.save(commit=False)
            event_detail.event = event
            event_detail.save()

            messages.success(request, "Event Updated Successfully")
            return redirect('/', self.object.id)
        return redirect('/', self.object.id)
    

"""
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

            event = event_form.save()
            event_detail = event_detail_form.save(commit=False)
            event_detail.event = event
            event_detail.save()

            messages.success(request, "Event Updated Successfully")
            return redirect('update-event', id)

    context = {"event_form": event_form, "event_detail_form": event_detail_form}
    return render(request, "event_form.html", context)"""

"""
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
        """
delete_event_decorators = [login_required, permission_required(
    "events.delete_event", login_url='no-permission')]
@method_decorator(delete_event_decorators, name='dispatch')
class DeleteEventView(DeleteView):
    model = Event
    success_url = reverse_lazy('dashboard')
    pk_url_kwarg = 'event_id'

"""
@login_required
@permission_required("events.view_event", login_url='no-permission')
def view_event(request):
    events = Event.objects.all()
    return render(request, "show_event.html", {"events": events})
"""
view_event_decorators = [login_required, permission_required(
    "events.view_event", login_url='no-permission')]

@method_decorator(view_event_decorators, name='dispatch')
class ViewEvent(ListView):
    model = Event
    context_object_name = 'events'
    template_name = 'show_event.html'

    def get_queryset(self):
        queryset = Event.objects.annotate(
            num_participants=Count('rsvp')).order_by('num_participants')
        return queryset

"""@login_required
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
"""
class EventDetail(DetailView):
    model = Event
    template_name = 'event_details.html'
    context_object_name = 'event'
    pk_url_kwarg = 'event_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # {"event": event}
        # {"event": event, 'status_choices': status_choices}
        context['status_choices'] = Event.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        selected_status = request.POST.get('event_status')
        event.status = selected_status
        event.save()
        return redirect('event-details', event.id)


@user_passes_test(is_participant, login_url='no-permission')
def add_rsvp(request, event_id, user_id):
    
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=event_id)
            user = User.objects.get(id=user_id)
        
            # Check if user has already RSVP'd
            if event.rsvp.filter(id=user_id).exists():
                messages.warning(request, f"User {user.username} has already RSVP'd for {event.name}")
                return redirect('participant-dashboard')
            # Add user to RSVP list
            event.rsvp.add(user)
            messages.success(request, f"User {user.username} has been added to the RSVP list for {event.name}")
            return redirect('participant-dashboard')
            
        except Event.DoesNotExist:
            messages.error(request, 'Event not found')
            return redirect('participant-dashboard')
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('participant-dashboard')
    else:
        messages.error(request, 'Invalid request method')
        return redirect('participant-dashboard')
        

@user_passes_test(is_participant, login_url='no-permission')
def rsvp_list(request, user_id):
    events = Event.objects.prefetch_related(
            Prefetch('rsvp', queryset=User.objects.filter(id=user_id), to_attr='all_rsvps')
        ).filter(rsvp=user_id)


    return render(request, 'rsvp/rsvp_list.html', {"events": events, "user_id": user_id})