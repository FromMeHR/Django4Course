from typing import Any
from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from products.models import Categories


class IndexView(TemplateView):
    template_name = "main/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Main'
        context['content'] = 'Furniture Store'
        return context
    

class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About'
        context['content'] = 'About'
        context['text_on_page'] = 'Text on this page'
        return context
    
    
# def index(request):
#     categories = Categories.objects.all()
#     context = { # better add in db new table
#         'title':'Main',
#         'content':'Furniture Store',
#         'categories':categories
#     }
#     return render(request, 'main/index.html', context)

# def about(request):
#     context = {
#         'title':'About', 
#         'content':'About',
#         'text_on_page':'Text on this page'

#     }
#     return render(request, 'main/about.html', context)