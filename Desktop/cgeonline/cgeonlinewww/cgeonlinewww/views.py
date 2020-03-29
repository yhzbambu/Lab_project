from django.http import HttpResponse
#from .models import do_something,county,location,our_picture,our_writer,showlist,Year,Month,Day,things
#from xiuyun import forms
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from .form import LoginForm,RegForm

# Create your views here
@login_required(login_url = '/login/') 
def homepage(request):
    return render(request,'homepage.html',locals())

def login(request):
    user_all = User.objects.all()
    name = request.POST.get('username')
    password = request.POST.get('password')
    try:
        user = auth.authenticate(username=name, password=password) #使用者驗證
    except:
        user = None
    if user is not None:         #若驗證成功，以 auth.login(request,user) 登入
        if user.is_active:
            auth.login(request,user) #登入成功
            return render(request, 'homepage.html', locals()) # 輸出到網頁上  #登入成功產生一個 Session，重導到<index.html>
            message = '登入成功!'
        else:
            message = '帳號尚未啟用!'
    else:
        message = '登入失敗!'
    return render(request,"sign.html",locals())  #登入失敗則重導回<login.html>

def register(request):
    if request.method =="POST":
        reg_form =RegForm(request.POST)
        if reg_form.is_valid():
            username=reg_form.cleaned_data['username']
            email=reg_form.cleaned_data['email']
            password=reg_form.cleaned_data['password']

            user=User.objects.create_user(username,email,password)
            user.save()

            user=auth.authenticate(username=username,password=password)
            auth.login(request,user)

            return redirect(request.GET.get('from',reverse('home')))

    else:        
        reg_form = RegForm()
        
    context={}
    context['reg_form']=reg_form
    return render(request,'register.html',context)

def logout(request):
    auth.logout(request)  #登出成功清除 Session，重導到<login.html>
    user_all = User.objects.all()
    name = request.POST.get('username')
    password = request.POST.get('password')
    return redirect('/')
