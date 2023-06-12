from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import UserProfile

def frontpage(request):
    return render(request,'core/frontpage.html')

@login_required(login_url='/user/login')
def dashboard(request, uname):
    user = User.objects.get(username=uname)
    request.session['uname'] = user.username
    user_profile = UserProfile.objects.get(user=user)
    context = {
        'data':uname,
        'user':user,
        'profile':user_profile,
    }
    return render(request,'core/dashboard.html',context)

@login_required(login_url='/user/login')
def EditProfile(request,uname):
    uname = request.session['uname']
    user  = user = User.objects.get(username=uname)
    user_profile = UserProfile.objects.get(user=user)
    context = {
        'data':uname,
        'user':user,
        'profile':user_profile,
    }
    return render(request,'core/editProfile.html',context)

@login_required(login_url='/user/login')
def Settings(request,uname):
    uname = request.session['uname']
    user  = user = User.objects.get(username=uname)
    user_profile = UserProfile.objects.get(user=user)
    context = {
        'data':uname,
        'user':user,
        'profile':user_profile,
    }
    return render(request,'core/settings.html',context)