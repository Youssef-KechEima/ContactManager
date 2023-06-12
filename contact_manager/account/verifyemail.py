from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

def send_email_token(email,token):
    try:
        user = User.objects.get(email=email)
        subject = 'Email Verification'
        message = f"Hi {user.username}, thank for your registration in ContactManager<br/> To verify your email <a href='http://localhost:8000/user/verify/{token}'>click Here</a> or copy this link http://localhost:8000/user/verify/{token}"
        msg = EmailMessage(subject=subject,body=message,to=[email])
        msg.content_subtype = 'html'
        msg.send()
    except Exception as e:
        return False
    return True

def send_email_token_resetPassword(email,token):
    try:
        user = User.objects.get(email=email)
        subject = 'Reset Password'
        message = f"Hi {user.username}<br/> To reset your Password <a href='http://localhost:8000/user/new_password/{token}'>click Here</a> or copy this link http://localhost:8000/user/new_password/{token}"
        msg = EmailMessage(subject=subject,body=message,to=[email])
        msg.content_subtype = 'html'
        msg.send()
    except Exception as e:
        return False
    return True