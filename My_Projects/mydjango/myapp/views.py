from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request,'home.html',{})

def index2(request):
    return render(request,'about.html',{})

def index3(request):
    return render(request,'contact.html',{})

def index4(request):
    return render(request,'education.html',{})
# Create your views here.
