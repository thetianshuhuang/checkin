"""
"""

from .models import Program, Record
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def add_record(record, program):

    # Check if ID exists
    if "record_id" not in record:
        return "error: no record ID"

    # Check if record alread present
    record_src = Record.objects.filter(
        program_id=program, record_id=record["record_id"])

    # Check valid type
    if record.get("type"):
        if record["type"] not in ["TASK", "ERR", "WARN", "INFO", "META"]:
            return "error: invalid type"

    # Assemble fields
    fields = {
        n: record.get(n) for n in
        ["parent", "name", "desc", "node_id", "type", "start", "end"]
    }
    meta = record.get("meta")
    fields["meta"] = json.dumps(meta) if meta else None

    # Create new
    if len(record_src) == 0:
        Record.objects.create(
            program=Program.objects.get(pk=program),
            record_id=record["record_id"],
            **fields)
    # Update existing
    else:
        record_src.update(
            **{k: v for k, v in fields.items() if v is not None})


def add_records(request, program):
    """
    {
        "records": [
            {
                "node_id": <MAC>,
                "record_id": <uuid>,
                "parent": <uuid>,
                "name": <str>,
                "desc": <str>,
                "type": <TASK|ERR|WARN|INFO|META>,
                "start": <datetime>,
                "end": <datetime>,
                "meta": <json>,
            },
            ...
        ]
    }
    """

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return {"error": "invalid JSON"}

    # Check authentication
    try:
        program = Program.objects.get(pk=program)
    except ObjectDoesNotExist:
        return {"error": "program does not exist"}
    if request.GET.get('token') != program.api_token:
        return {"error": "invalid token"}

    # Check mandatory keys
    if type(body.get("records")) != list:
        return {"error": "POST body must contain 'records' entry"}

    # Add records
    status = [add_record(record, program.id) for record in body["records"]]
    return {"success": status}


@csrf_exempt
def view_add_records(request, program):
    return JsonResponse(add_records(request, program))
