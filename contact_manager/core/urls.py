from django.urls import path
from . import views

urlpatterns = [
    path('',views.frontpage,name="frontpage"),
    path('<str:uname>/dashboard/',views.dashboard,name='dashboard'),
    path('<str:uname>/edit_profile/',views.EditProfile,name='edit_profile'),
    path('<str:uname>/settings/',views.Settings,name='settings'),
]