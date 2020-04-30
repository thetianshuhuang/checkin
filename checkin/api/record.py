"""Record management API"""

import json
import secrets

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from .models import Record, Program
from .util import json_response, serialize_objects


def add_record(record, program):
    """Add a single record.

    Parameters
    ----------
    record : dict
        Record dictionary. See below for format.
    program : int
        Target program id

    Returns
    -------
    str
        Status.
    """

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

    # Not root and does not already exist
    if len(record_src) == 0 and record.get("parent") != program:

        # Make sure parent exists.
        try:
            Record.objects.get(
                program_id=program, record_id=record.get("parent"))
        except ObjectDoesNotExist:
            return "error: invalid parent"

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

    return "success"


@csrf_exempt
@json_response
def new(request, program):
    """API to create new records.

    Parameters
    ----------
    request : Django request.
        Should have the GET parameter 'token', which should be the program API
        token.
        The POST json payload should take the following format:
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
    program : int
        Program ID.

    Returns
    -------
    JsonResponse
        Indicates success or error. Possible status codes:
        - 400: Invalid JSON or JSON does not contain 'records' entry
        - 401: Invalid token
        - 404: Invalid program ID
        - 200: Success. Note that individual records may fail, while the
            request as a whole returns success.
    """

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return {"error": "invalid JSON"}, 400

    # Check authentication
    try:
        program = Program.objects.get(pk=program)
    except ObjectDoesNotExist:
        return {"error": "program does not exist"}, 404
    if not secrets.compare_digest(request.GET.get('token'), program.api_token):
        return {"error": "invalid token"}, 401

    # Check mandatory keys
    if type(body.get("records")) != list:
        return {"error": "POST body must contain 'records' entry"}, 400

    # Add records
    status = [add_record(record, program.id) for record in body["records"]]
    return {"success": status}, 200


@json_response
def get(request, program):
    """Get records corresponding to a program.

    Parameters
    ----------
    request : Django request
        Should have the GET parameter 'token', which is the program access
        token.
    program : int
        Program ID

    Returns
    -------
    JsonResponse
        Same format as records/new, except in case of error.
        Possible status codes:
        - 401: Invalid token
        - 404: Invalid program
        - 200: Success
    """

    # Check authentication
    try:
        program = Program.objects.get(pk=program)
    except ObjectDoesNotExist:
        return {"error": "program does not exist"}, 404
    if not secrets.compare_digest(
            request.GET.get('token'), program.access_token):
        return {"error": "invalid token"}, 401

    fields = [
        "record_id", "parent", "name", "desc", "node_id", "type", "start",
        "end", "meta"
    ]

    return {
        "records": serialize_objects(
            Record.objects.filter(program_id=program), fields)
    }, 200
