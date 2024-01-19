from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse
from products.models import Categories

def index(request):
    categories = Categories.objects.all()
    context = { # better add in db new table
        'title':'Main',
        'content':'Furniture Store',
        'categories':categories
    }
    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title':'About', 
        'content':'About',
        'text_on_page':'Text on this page'

    }
    return render(request, 'main/about.html', context)