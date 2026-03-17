from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView, TemplateView
from attendance import views



urlpatterns = [
    
    path('',TemplateView.as_view(template_name='base.html'), name='base'),
    path('post-login/',views.post_login_redirect,name="post_login_redirect"),
    path('register/', views.register_view, name='register'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name = 'registration/logged_out.html', next_page ='base'), name='logout'),
    path('scan_qr_auto/', views.check_in_view, name='scan_qr_auto'),
    path('check-in/', views.check_in, name='check_in'),
    path('checked-in/', views.checked_in_page, name='scan_checked_in'),
    path('checked-out/', views.checked_out_page, name='scan_checked_out'),
    path('wait/',views.wait_for_checkout_page, name='scan_wait_for_checkout'),
    path('already-out', views.already_checked_out_page, name='scan_already_checked_out'),
    path('daily-logs/', views.daily_logs, name='daily_logs'),
    path('teacher-home/', views.teacher_home_view, name='teacher_home'),
    path('qrcode_download', views.download_qr_page,name='qrcode_download'),
    path('pdf/', views.export_pdf, name='pdf'),
     path('teacher-pdf/', views.teacher_pdf, name='teacher-pdf'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # path("timetables/",TimetableListView.as_view(), name="timetables_list.html"), 
]
