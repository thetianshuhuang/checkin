import requests


records = [
    {
        "program": "12345678-1234-1234",
        "name": "Program Name",
        "desc": "Program description",
        "start": 12345,
        "end": None,
        "record_id": "10",
        "parent": "12345678-1234-1234",
        "type": "TASK"
    },
    {
        "record_id": "11",
        "name": "Test Parent",
        "desc": "Test description",
        "node_id": "00",
        "type": "TASK",
        "start": 12345,
        "end": None,
        "meta": None,
        "parent": "10"
    },
    {
        "record_id": "12",
        "name": "Test Info",
        "desc": "Info description",
        "node_id": "00",
        "type": "INFO",
        "start": 12345,
        "end": 12345,
        "meta": None,
        "parent": "11",
    },
    {
        "record_id": "19",
        "name": "Test Warning",
        "desc": "Warning metadata and information",
        "node_id": "00",
        "type": "WARN",
        "start": 12345,
        "end": 12345,
        "meta": None,
        "parent": "11",
    },
    {
        "record_id": "13",
        "name": "Test Error",
        "desc": "Error traceback\netc",
        "node_id": "00",
        "type": "ERR",
        "start": 12345,
        "end": 12345,
        "meta": None,
        "parent": "14",
    },
    {
        "record_id": "14",
        "name": "Queued Task",
        "desc": "This task is not yet running.",
        "node_id": "00",
        "type": "TASK",
        "start": None,
        "end": None,
        "meta": None,
        "parent": "10",
    },
    {
        "record_id": "11",
        "end": 12345,
    },
]

r = requests.post(
    "http://localhost:8000/api/new/1",
    params={"token": "abc123"},
    json={"records": records})
print(r.content)
