from django.urls import path
from . import node
from . import client


urlpatterns = [
    path('new/<program>', node.view_add_records),
    path('get/<program>', client.get_records),
    path('programs', client.list_programs)
]
