from django.urls import path
from .views import signup_view, UserLogin, logout_view, profile_view, send_message
from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


#app_name = 'user'
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    path('message/', send_message, name='message')
]
