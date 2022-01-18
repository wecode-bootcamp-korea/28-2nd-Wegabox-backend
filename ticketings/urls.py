from django.urls import path
from ticketings.models import Ticketing

from ticketings.views import TicketingView

urlpatterns = [
    path('',TicketingView.as_view()),
]