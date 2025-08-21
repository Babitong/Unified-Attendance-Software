"""
URL configuration for HINETEC_ATTENDANCE_SYSTEM project.

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
from django.urls import path, include
from users.admin import admin_site 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView, TemplateView
from attendance import views



urlpatterns =[
    

    path ('admin/',admin_site.urls),
    path('accounts/',include('users.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
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
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
   
    

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
