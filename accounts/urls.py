from django.urls.conf import include
from accounts.utils import login_forbidden
from re import template
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.signin, name='login'),
    path('verify/', views.verify, name='verify'),
    path('logout/', views.signout, name='logout'),
    path('register/', views.signup, name='register'),
    path('resend_verification/', views.resend, name='resend'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path(
        'password_change/', 
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/change-password.html',
            success_url = reverse_lazy('accounts:password_change_done')
        ), 
        name='password_change'
    ),
    path(
        'password_change/done/', 
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password-change-done.html',
        ), 
        name='password_change_done'
    ),
    path(
        'password_reset/', 
        login_forbidden(
            auth_views.PasswordResetView.as_view(
                template_name='accounts/password-reset.html',
                html_email_template_name='accounts/password-reset-html-email.html',
                email_template_name= 'accounts/example_message.txt',
                success_url = reverse_lazy('accounts:password_reset_done')
            ),
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/', 
        login_forbidden(
            auth_views.PasswordResetDoneView.as_view(
                template_name='accounts/password-reset-done.html',
            ), 
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/', 
        login_forbidden(
            auth_views.PasswordResetConfirmView.as_view(
                template_name='accounts/password-reset-confirm.html',
                success_url=reverse_lazy('accounts:password_reset_complete')
            ),
        ), 
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        login_forbidden(
            auth_views.PasswordResetCompleteView.as_view(
                template_name='accounts/password-reset-complete.html'
            ), 
        ),
        name='password_reset_complete'
    ),
]