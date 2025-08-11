from django.views.generic import TemplateView

from core.mixins import OperatorRequiredMixin


class TerminalView(OperatorRequiredMixin, TemplateView):
    template_name = 'terminal/terminal.html'
