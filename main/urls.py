from main.views import *
from django.urls import path, include

app_name = 'main'
urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),

]