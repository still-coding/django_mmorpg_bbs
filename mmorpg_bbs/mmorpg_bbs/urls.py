"""
URL configuration for mmorpg_bbs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from user_profiles import views as user_profiles_views

urlpatterns = [
    path('', include('bbs.urls', namespace='bbs')),
    path('profile/', include('user_profiles.urls', namespace='user_profiles')),
    path('sign_up/', user_profiles_views.sign_up, name='sign_up'),
    path('sign_in/', user_profiles_views.sign_in, name='sign_in'),
    path('sign_out/', user_profiles_views.sign_out, name='sign_out'),
    path('otp_check/', user_profiles_views.otp_check, name='otp_check'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    