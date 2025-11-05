from django.shortcuts import render
from django.template import TemplateDoesNotExist

def page_handler(request, template):
    try:
        return render(request, template)
    except TemplateDoesNotExist:
        return render(request, 'easebuzz/page_not_available.html', {"page": template})
