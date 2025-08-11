from django.urls import path
from apps.terminal.views import (
    TerminalView
)

app_name = "terminal"


urlpatterns = [
    path('dashboard/', TerminalView.as_view(), name='terminal_dashboard'),
]
