from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from .verifyemail import send_email_token,send_email_token_resetPassword
from .models import EmailVerification,UserProfile
import uuid

def RegisterPage(request):
    if request.method == 'POST':
        Firstname = request.POST['Firstname']
        Lastname = request.POST['Lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 =  request.POST['password2']
        if password2 != password:
            messages.warning(request,'Password does not match !')
        if len(Firstname) < 6:
            messages.warning(request,'the Firstname must have more than 6 characters!')
        if len(Lastname) < 6:
            messages.warning(request,'the Lastname must have more than 6 characters!')
        if len(username) < 6:
            messages.warning(request,'the username must have more than 6 characters!')
        if len(password) < 8:
            messages.warning(request,'the password must have more than 8 characters!')
        
        else:
            if User.objects.filter(email=email,username=username).exists():
                messages.warning(request,'User already exists!')
            else:
                try:
                    myuser = User.objects.create_user(username=username,email=email,password=password)
                    myuser.first_name = Firstname
                    myuser.last_name = Lastname
                    myuser.save()
                    email_obj = EmailVerification.objects.create(
                        user = myuser,
                        auth_token = str(uuid.uuid4())
                    )
                    user_profile = UserProfile.objects.create(user=myuser)
                    user_profile.addresses = None
                    user_profile.phone_number = None
                    send_email_token(email,email_obj.auth_token)
                    messages.success(request,'Account created successfully, please verify your email!')
                    return redirect('login')
                except:
                    messages.warning(request,'something went wrong, try again!')
                    return redirect('register')     
            
    return render(request,'account/registerPage.html')

def verify(request, token):
    try:
        obj = EmailVerification.objects.get(auth_token=token)
        obj.is_verified = True
        obj.save()
        messages.success(request,'Your Email is Verified')
        return redirect('login')
    except:
        messages.warning(request,'Something went wrong')
        redirect('login')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST.get('password')    
        user = authenticate(username=username, password=passwd)     
        if user is not None:
            obj_user = EmailVerification.objects.get(user=user)
            if obj_user.is_verified == True:    
                login(request, user)
                uname = user.username
                return redirect('dashboard',uname)
            else:
                messages.warning(request,'Please verify your email before log in!')
        else:
            messages.warning(request,'Email or Password is incorrect !')
    return render(request,'account/loginPage.html')

def LogOutPage(request):
    logout(request)
    messages.success(request,'You have log out successfully !')
    return redirect('login')

def restPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user =User.objects.get(email=email)
            obj_email = EmailVerification.objects.get(user=user)
            send_email_token_resetPassword(email,obj_email.auth_token)
            messages.success(request,'Email sent successfully')
            return redirect('reset_password')
        except:
            messages.warning(request,'Email does not exist') 

    return render(request,'account/resetPassword.html')

def newPassword(request,token):
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if new_password != new_password2:
                messages.warning(request,'Password does not match')
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password Changed successfully')
                return redirect('login')
        except:
            messages.warning(request,'email does not exist')

    return render(request,'account/newPassword.html',{'tk':token})
