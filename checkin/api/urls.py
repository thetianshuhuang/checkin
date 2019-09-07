from django.urls import path
from . import node
from . import client

from django.http import JsonResponse


def api_404(request):
    return JsonResponse({"error": "unknown api"})


urlpatterns = [
    path('records/new/<program>', node.add_records),
    path('records/get/<program>', client.get_records),
    path('programs/new', node.create_program),
    path('programs/list', client.list_programs),

    path(r'.*/', api_404)
]
