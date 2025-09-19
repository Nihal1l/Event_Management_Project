from django.urls import path
from events.views import views


urlpatterns = [
    path('', views.home, name='home')
]
