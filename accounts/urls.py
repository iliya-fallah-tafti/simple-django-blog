from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile', views.profile_view, name='profile'),  # profile
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),  # edit_profile
    path('login', views.login_view, name='login'),  # login
    path('logout', views.logout_view, name='logout'),  # logout
    path('signup', views.signup_view, name='signup'),  # registration / signup
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset/<uidb64>/<token>/', views.reset_password, name='reset_password'),
]
