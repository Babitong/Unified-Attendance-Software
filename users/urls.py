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
    path('change-password/', views.change_password, name='change_password'),
    
    path('accounts/login/',auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name = 'registration/logged_out.html', next_page ='base'), name='logout'),
    path('scan_qr_auto/', views.check_in_view, name='scan_qr_auto'),
    path('check-in/', views.check_in, name='check_in'),
    path('checked-in/', views.checked_in_page, name='scan_checked_in'),
    path('checked-out/', views.checked_out_page, name='scan_checked_out'),
    path('wait/',views.wait_for_checkout_page, name='scan_wait_for_checkout'),
    path('already-out', views.already_checked_out_page, name='scan_already_checked_out'),
    path('secretary-dashboard/', views.secretary_dashboard, name='secretary_dashboard'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('qrcode_download', views.download_qr_page,name='download_qr_page'),
    path('pdf/', views.export_pdf, name='pdf'),
    path('employee-export/', views.employee_export, name='employee_export'),
    path('report-view/', views.report_view, name='report_view'),


        path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
     
]
