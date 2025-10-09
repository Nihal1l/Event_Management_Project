from django.urls import path
from users.views import *
from events.views import *

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('dashboard/admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('dashboard/organizer-dashboard/', OrganizerDashboardView.as_view(), name="organizer-dashboard"),
    path('dashboard/participant-dashboard/', ParticipantDashboardView.as_view(), name="participant-dashboard"),
    path('create-event/', CreateEvent.as_view(), name='create-event'),
    path('view-event/', ViewEvent.as_view(), name='view-event'),
    path('event-details/<int:event_id>/', EventDetail.as_view(), name='event-details'),
    path('update-event/<int:event_id>/', UpdateEvent.as_view(), name='update-event'),
    path('delete-event/<int:event_id>/', DeleteEventView.as_view(), name='delete-event'),
    path('add_rsvp/<int:event_id>/<int:user_id>/', add_rsvp, name='add-rsvp'),
    path('rsvp-list/<int:user_id>/', rsvp_list, name='rsvp-list')
]
