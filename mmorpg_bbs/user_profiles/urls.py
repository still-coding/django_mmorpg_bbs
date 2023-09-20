from django.urls import path

from .views import profile

app_name = 'user_profiles'

urlpatterns = [
    path('', profile, name='profile'),
]