

from .models import Program, Record, UserToken
from .util import json_response
from django.core.exceptions import ObjectDoesNotExist
import secrets


def serialize_objects(queryset, fields):

    return [
        {k: getattr(obj, k) for k in fields}
        for obj in queryset
    ]


@json_response
def get_records(request, program):

    # Check authentication
    try:
        program = Program.objects.get(pk=program)
    except ObjectDoesNotExist:
        return {"error": "program does not exist"}
    if not secrets.compare_digest(
            request.GET.get('token'), program.access_token):
        return {"error": "invalid token"}

    fields = [
        "record_id", "parent", "name", "desc", "node_id", "type", "start",
        "end", "meta"
    ]

    return {
        "records": serialize_objects(
            Record.objects.filter(program_id=program), fields)
    }


@json_response
def list_programs(request):

    # Check token
    try:
        user = UserToken.objects.get(api_token=request.GET.get('token')).owner
    except ObjectDoesNotExist:
        return {"error": "invalid token"}

    fields = ["api_token", "start", "end"]

    return {
        "programs": serialize_objects(
            Program.objects.filter(owner=user), fields)
    }
