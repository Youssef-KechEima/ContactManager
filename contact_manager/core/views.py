from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from account.models import UserProfile
from django.contrib import messages

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
    if request.method == 'POST':
        addresse = request.POST.get("addresse")
        phoneNumber = request.POST.get("phoneNumber")
        try:
            user_profile.addresses = addresse
            user_profile.phone_number = phoneNumber
            if len(request.FILES) != 0:
                user_profile.user_avatar = request.FILES['image']
            user_profile.save()
            messages.success(request,"Update successfully")
        except:
            messages.warning(request,"Something went wrong")
    context = {
        'data':uname,
        'user':user,
        'profile':user_profile,
    }
    return render(request,'core/editProfile.html',context)

@login_required(login_url='/user/login')
def Settings(request,uname):
    uname = request.session['uname']
    user = User.objects.get(username=uname)
    user_profile = UserProfile.objects.get(user=user)
    if request.method == "POST":
        current_passwd = request.POST.get('current_password')
        new_passwd = request.POST.get('new_password')
        confirm_new_passwd = request.POST.get('confirm_new_password')
        if check_password(current_passwd,user.password):
            if len(new_passwd) < 8:
                messages.warning(request,'password must have more than 8 characters')
            if new_passwd != confirm_new_passwd:
                messages.warning(request,'Password does not match !')
            else:
                user.set_password(new_passwd)
                user.save()
                logout(request)
                messages.success(request,'You have change your password please log in with your new password ')
                return redirect('login')
        else:
            messages.warning(request,'Current Password is incorrect !')
    context = {
        'data':uname,
        'user':user,
        'profile':user_profile,
    }
    return render(request,'core/settings.html',context)

@login_required(login_url='/user/login')
def DeleteAccount(request, uname):
    uname = request.session['uname']
    user  = User.objects.get(username=uname)
    user.delete()
    logout(request)
    messages.success(request,'You have Deleted your account')
    return redirect('login')