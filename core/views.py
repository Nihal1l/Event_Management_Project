from django.shortcuts import render

# Create your views here.


from events.models import Event

def home(request):
    events = Event.objects.all().order_by('-created_at')[:6]
    return render(request, 'home.html', {'events': events})

def no_permission(request):
    return render(request, 'no_permission.html')