from django.contrib import messages
from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Q, Count, Max, Min, Avg
# Create your views here.

def dynamic_dashboard(request):

    type = request.GET.get('type')
    search_query = request.GET.get('q','')
    if search_query:
        type = 'all'
        base_query = Event.objects.select_related(
            'category').prefetch_related('participants').annotate(participants_count=Count('participants')).filter(Q(name__icontains=search_query) | Q(location__icontains=search_query))
        counts = Event.objects.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='COMPLETED')),
            in_progress=Count('id', filter=Q(status='IN-PROGRESS')),
            pending=Count('id', filter=Q(status='PENDING'))
        )
        participants = Participant.objects.aggregate(
            total=Count('id')
        )
        context = {"counts": counts, "participants": participants, "events": base_query, "type": type}
        return render(request, "dynamic.html", context)
    print(type)

    # Retriving task data

    base_query = Event.objects.select_related(
        'category').prefetch_related('participants').annotate(participants_count=Count('participants'))
    
    if type == 'completed':
        base_query = base_query.filter(status='COMPLETED')
    elif type == 'upcoming':
        base_query = base_query.filter(date__gte=timezone.now().date())
    elif type == 'past':
        base_query = base_query.filter(date__lt=timezone.now().date())
    elif type == 'all':
        base_query = base_query.all()
    else:
        today = timezone.now().date()  # Use this instead
        tomorrow = today + timedelta(days=1)
        base_query = base_query.filter(date=tomorrow).order_by('time')

    counts = Event.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN-PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING'))
    )
    participants = Participant.objects.aggregate(
        total=Count('id')
    )

    

    context = {"counts": counts, "participants": participants, "events": base_query, "type": type}

    return render(request, "dynamic.html", context)



def create_event(request):
    # employees = Employee.objects.all()
    form = EventModelForm()  # For GET

    if request.method == "POST":
        form = EventModelForm(request.POST)
        if form.is_valid():

            """ For Model Form Data """
            form.save()

            return render(request, 'event_form.html', {"form": form, "message": "event added successfully"})

            ''' For Django Form Data'''
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')  # list [1,3]

            # task = Task.objects.create(
            #     title=title, description=description, due_date=due_date)

            # # Assign employee to tasks
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)

            # return HttpResponse("Task Added successfully")

    context = {"form": form}
    return render(request, "event_form.html", context)


def update_event(request, event_id):
    event = Event.objects.get(id=event_id)
    form = EventModelForm(instance=event)

    if request.method == "POST":
        form = EventModelForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('update-event', event.id)
        

    context = {"form": form}
    return render(request, "event_form.html", context)

def delete_event(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(id=event_id)
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return redirect('dynamic')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('dynamic')

