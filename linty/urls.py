from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url('', include('interface.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
]
