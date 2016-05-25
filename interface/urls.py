from django.conf.urls import url

from interface.views import ResultDetailView

urlpatterns = [
    url(r'^result/(?P<pk>[0-9]+)$', ResultDetailView.as_view(), name='result_detail'),
]