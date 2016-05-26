from django.conf.urls import url

from interface.views import BuildDetailView, WebhookView

urlpatterns = [
    url(r'^build/(?P<pk>[0-9]+)$', BuildDetailView.as_view(), name='build_detail'),
    url(r'^webhook$', WebhookView, name='webhook')
]
