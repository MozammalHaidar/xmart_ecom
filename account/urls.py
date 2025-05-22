from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('Forget_pass/', views.Forget_pass, name='Forget_pass'),
    path('verify-reset-otp/', views.reset_password_otp, name='reset_password_otp'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('update_profile/', views.update_profile, name='update_profile'),
]
