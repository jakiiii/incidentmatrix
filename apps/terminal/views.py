from django.views.generic import TemplateView


class TerminalView(TemplateView):
    template_name = 'terminal/terminal.html'
