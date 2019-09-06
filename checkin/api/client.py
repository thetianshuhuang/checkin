

from .models import Program, Record
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


def serialize_objects(queryset, fields):

    return [
        {k: getattr(obj, k) for k in fields}
        for obj in queryset
    ]


def get_records(request, program):

    # Check authentication
    try:
        program = Program.objects.get(pk=program)
    except ObjectDoesNotExist:
        return {"error": "program does not exist"}
    if request.GET.get('token') != program.api_token:
        return {"error": "invalid token"}

    fields = [
        "record_id", "parent", "name", "desc", "node_id", "type", "start",
        "end", "meta"
    ]

    return JsonResponse({
        "records": serialize_objects(
            Record.objects.filter(program_id=program), fields)})


def list_programs(request):

    fields = ["api_token", "share_token", "start", "end"]

    return JsonResponse({
        "programs": serialize_objects(
            Program.objects.filter(owner=request.user), fields)})
