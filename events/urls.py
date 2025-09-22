from django.urls import path
from .views import *


urlpatterns = [
    path('create_event/', create_event, name='create-event'),
    path('update_event/<int:event_id>/', update_event, name='update-event'),
    path('delete_event/<int:event_id>/', delete_event, name='delete_event'),
    path('', dynamic_dashboard, name='dynamic'),
]
