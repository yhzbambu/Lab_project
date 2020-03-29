from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import datetime
# Create your views here.

def home(request):
    return render(request,"index.html",locals())

def homepage(request):
    return render(request,"homepage.html",locals())

