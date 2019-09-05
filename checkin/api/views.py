from django.shortcuts import render


# Create your views here.


"""
+--------+
|Node API|
+--------+

Packet may have multiple data entries.

META type is special; indicates program or node information.
For META type, only "type" and "meta" are present.

POST with JSON
--------------
{
    "program": <id>,
    "node_id": <MAC>,
    "token": <api token>,
    "data": [
        {
            "record_id": <uuid>,
            "parent": <uuid>,
            "name": <str>,
            "desc": <str>,
            "type": <TASK|ERR|WARN|INFO|META>,
            "start": <datetime>,
            "end": <datetime>,
            "meta": <json>
        },
        ...
    ]
}

On receipt
----------
Check if program exists, and that API token matches program ID. If not,
    return 401.
Check if node_id exists in RunNodes. If not, add the node to RunNodes.
For entry in "data":
    If type == META:
        update the RunNodes information.
    Else:
        If record_id exists:
            Update all present keys
        Else:
            Create new record


If the record_id does not exist, a new record is created.
Otherwise, all present keys are updated.

+----------+
|Client API|
+----------+

GET with login cookies, program ID in URL. Returns JSON.

Return JSON
-----------
{
    "program": <id>,
    "start": <datetime|null>,
    "end": <datetime|null>,
    "data": [
        {
            "record_id": <uuid>,
            "name": <str>,
            "desc": <str>,
            "node_id": <str>,
            "type": <TASK|ERR|WARN|INFO>,
            "start": <datetime|null>,
            "end": <datetime|null>,
            "meta": <json>,
            "children": [
                {
                    ...
                },
                ...
            ]
        },
        ...
    ]
}

HTML elements should have ID:
[record-id]-[element-name]

When drawing, first check if the element exists:
document.getElementById(record_id)

If it exists, update the elements:
document.getElementById(record_id + "name"),
document.getElementById(record_id + "progress"), etc

Proceed recursively so that the parent always exists:

def draw(record):

    if record exists:
        update record
    else:
        create record

    for child in record.children:
        draw(child)
"""
