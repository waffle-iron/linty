from django.conf.urls import url

from interface.views import BuildDetailView, WebhookView, RegisterRepoView

urlpatterns = [
    url(r'^build/(?P<pk>[0-9]+)$', BuildDetailView.as_view(), name='build_detail'),
    url(r'^add$', RegisterRepoView.as_view(), name='register_repo'),
    url(r'^webhook$', WebhookView, name='webhook')
]
