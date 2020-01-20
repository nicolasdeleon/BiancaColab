"""backBone_Bianca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from .views import (
    home_view,
    contacto_view,
    quienes_somos_view,
    user_list_view,
    usersToBeAccepted_view,
)

from eventos.views import (
    blog_post_create_view, 
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('contacto', contacto_view),
    path('quienes-somos', quienes_somos_view),
    path('eventos/',include('eventos.urls')),
    path('Create-Event',blog_post_create_view),
    path('Users',user_list_view),
    path('users-to-be-accepted', usersToBeAccepted_view),

    #ACCOUNTS VIEWS
    path('accounts/', include('accounts.urls')),

    #REST FRAMEWORK URLS
    path('api/eventos/',include('eventos.api.urls')),
    path('api/accounts/',include('accounts.api.urls'))

]

if settings.DEBUG:
    #test mode
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT) 
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)