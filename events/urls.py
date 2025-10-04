from django.urls import path
from users.views import *
from events.views import *

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('dashboard/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('dashboard/organizer-dashboard/', organizer_dashboard, name="organizer-dashboard"),
    path('dashboard/participant-dashboard/', participant_dashboard, name="participant-dashboard"),
    path('create-event/', create_event, name='create-event'),
    path('view-event/', view_event, name='view-event'),
    path('event-details/<int:event_id>/', event_details, name='event-details'),
    path('update-event/<int:event_id>/', update_event, name='update-event'),
    path('delete-event/<int:event_id>/', delete_event, name='delete-event'),
]
