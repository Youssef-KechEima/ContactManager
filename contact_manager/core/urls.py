from django.urls import path
from . import views

urlpatterns = [
    path('',views.frontpage,name="frontpage"),
    path('<str:uname>/dashboard/',views.dashboard,name='dashboard'),
    path('<str:uname>/edit_profile/',views.EditProfile,name='edit_profile'),
    path('<str:uname>/settings/',views.Settings,name='settings'),
    path('<str:uname>/delete_account/',views.DeleteAccount,name="delete_account"),
    path('<str:uname>/insert/',views.insert,name="insert"),
    path('<str:uname>/delete/<str:id>',views.Delete,name='delete'),
    path('<str:uname>/edit/<str:id>',views.Edit,name='edit'),
]