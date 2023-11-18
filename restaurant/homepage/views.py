from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    TEMPLATE = "homepage/main.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.TEMPLATE)
