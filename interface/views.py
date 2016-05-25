from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from interface.models import Result


class ResultDetailView(DetailView):
    model = Result


@csrf_exempt
def WebhookView(request):
    return HttpResponse(status=204)
