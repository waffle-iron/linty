from django.conf.urls import url

from interface.views import ResultDetailView, WebhookView

urlpatterns = [
    url(r'^result/(?P<pk>[0-9]+)$', ResultDetailView.as_view(), name='result_detail'),
    url(r'^webhook$', WebhookView, name='webhook')
]
