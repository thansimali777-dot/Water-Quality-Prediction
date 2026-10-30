"""
URL configuration for water_quality_prediction_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login_get/',views.login_get),
    path('logins_post/',views.logins_post),
    path('adminhome/',views.adminhome),
    path('user_register_get/',views.user_register_get),
    path('user_register_post/',views.user_register_post),
    path('view_user_register/',views.view_user_register),
    path('edituser/<id>',views.edituser),
    path('edituserpost/',views.edituserpost),
    path('deleteuser/<id>',views.deleteuser),
    path('waterquality/',views.waterquality),
    path('waterqualitypost/',views.waterqualitypost),
    path('viewresult/',views.viewresult),
    path('feedback/',views.feedback),
    path('feedbackpost/',views.feedbackpost),
    path('viewfeedback/',views.viewfeedback),
    path('replycomplaint/<id>', views.replycomplaint),
    path('replycomplaintpost/', views.replycomplaintpost),
    path('userhome/', views.userhome),
    path('',views.home),
    path('sendcomplaint/',views.sendcomplaint),
    path('complaintpost/',views.complaintpost),
    path('viewcomplaint/',views.viewcomplaint),
    path('editcomplaintpost/',views.editcomplaintpost),
    path('deletecomplaint/<id>',views.deletecomplaint),
    path('editcomplaint/<id>',views.editcomplaint),
    path('admin_view_complaints/',views.admin_view_complaints),

]
