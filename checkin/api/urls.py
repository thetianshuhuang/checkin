from django.urls import path

from . import token
from . import record
from . import program

from django.http import JsonResponse


def api_404(request):
    return JsonResponse({"error": "unknown api"})


urlpatterns = [
    path('records/new/<program>', record.new),
    path('records/get/<program>', record.get),

    path('programs/new', program.create),
    path('programs/list', program.list),
    path('programs/delete/<program>', program.delete),

    path('tokens/delete', token.delete),
    path('tokens/new', token.new),

    path(r'.*/', api_404)
]
