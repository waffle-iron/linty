from django.views.generic import DetailView

from interface.models import Result


class ResultDetailView(DetailView):
    model = Result


