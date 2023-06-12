from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.LoginPage,name='login'),
    path('register/',views.RegisterPage,name='register'),
    path('logout/',views.LogOutPage,name='logout'),
    path('verify/<str:token>', views.verify),
    path('reset_password/',views.restPassword,name='reset_password'),
    path('new_password/<str:token>',views.newPassword,name='new_password'),
]