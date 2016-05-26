from django.conf.urls import url, include

urlpatterns = [
    url('', include('interface.urls')),
    url('', include('social.apps.django_app.urls', namespace='social'))
]
