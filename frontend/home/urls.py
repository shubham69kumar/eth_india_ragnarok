from django.conf.urls import url, include
from django.contrib import admin
from django.shortcuts import render, redirect
from django.views.generic import RedirectView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('meta_mask' , views.metamask , name = 'meta_mask'),
    path('signup' , views.signup,name = "signup"),
    path('signin' , views.home_view , name= "signin"),
    path('student_reg' , views.register , name = 'student_reg'),
    path('main_student' , views.student_data , name = 'main_student'),
    path('sig_up' , views.sign_in , name = 'sig_up'),
    path('student_auth' , views.stu_auth , name = 'student_auth'),
    path('teacher_auth' , views.teach_auth , name = 'teacher_auth'),

    
]
