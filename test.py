import requests
import json


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
        "desc": "Error traceback\netc;\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
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

b = requests.get(
    "http://localhost:8000/api/programs/new",
    params={"token": "test_token_123", "name": "test program"})
res = json.loads(b.content)


token_record = res["api_token"]
token_view = res["access_token"]
pid = res["id"]

print(pid)
print(token_view)
print(token_record)


r = requests.post(
    "http://localhost:8000/api/records/new/" + str(pid),
    params={"token": token_record},
    json={"records": records})
print(r.content)
