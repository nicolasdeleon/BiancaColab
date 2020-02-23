from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from eventos.views import blog_post_create_view

from .views import (contacto_view, home_view, quienes_somos_view,
                    user_list_view, usersToBeAccepted_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('contacto', contacto_view),
    path('quienes-somos', quienes_somos_view),
    path('eventos/', include('eventos.urls')),
    path('Create-Event', blog_post_create_view),
    path('Users', user_list_view),
    path('users-to-be-accepted', usersToBeAccepted_view),

    # ACCOUNTS VIEWS
    path('accounts/', include('accounts.urls')),

    # REST FRAMEWORK URLS
    path('api/eventos/', include('eventos.api.urls')),
    path('api/accounts/', include('accounts.api.urls'))
]

if settings.DEBUG:
    # In DEBUG / Test Mode
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
