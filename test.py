import requests
import json
import uuid
import time


class Record:

    def __init__(
            self,
            program=None,
            name="Generic Record",
            desc="",
            parent=None,
            record_id=None,
            type="TASK"):

        self.program = program
        self.record_id = str(uuid.uuid4()) if record_id is None else record_id
        self.parent = program if parent is None else parent
        self.name = name
        self.desc = desc

        # Task has start, end time
        if type == "TASK":
            self.start_time = None
            self.end_time = None
        # ERR/WARN/INFO has time fixed at now with 0 duration
        else:
            self.start_time = time.time()
            self.end_time = self.start_time

        self.type = type

    def subrecord(self, name="Generic Sub-Record", desc="", type="TASK"):
        return Record(
            program=self.program,
            name=name,
            desc=desc,
            parent=self.record_id,
            type=type)

    def subtask(self, **kwargs):
        return self.subrecord(type="TASK", **kwargs)

    def error(self, **kwargs):
        return self.subrecord(type="ERR", **kwargs)

    def warning(self, **kwargs):
        return self.subrecord(type="WARN", **kwargs)

    def info(self, **kwargs):
        return self.subrecord(type="INFO", **kwargs)

    def dict(self):
        return {
            "program": self.program,
            "name": self.name,
            "desc": self.desc,
            "type": self.type,
            "start": self.start_time,
            "end": self.end_time,
            "meta": None,
            "parent": self.parent,
            "record_id": self.record_id
        }

    def start(self):
        if self.start_time is not None:
            raise Exception(
                "Could not mark start time: record already started")
        self.start_time = time.time()

        return self

    def done(self):
        if self.start_time is None:
            raise Exception(
                "Could not mark finish time: record not yet started")
        if self.end_time is not None:
            raise Exception(
                "Could not mark finish time: record already done")
        self.end_time = time.time()

        return self

    @property
    def duration(self):
        if self.end_time is None or self.start_time is None:
            return 0
        else:
            return self.end_time - self.start_time


class Program(Record):

    def __init__(
            self, server=None, name=None, program=None, api_token=None,
            user_token=None,
            **kwargs):

        if server is None:
            raise Exception("Must provide a server.")

        self.server = server

        # Request new program
        if program is None:
            r = requests.get(
                "{}/api/programs/new".format(server),
                params={"token": user_token, "name": name})
            if r.status_code != 200:
                raise Exception(
                    "Server did not return success (200):\n" + r.content)

            # Save program details
            res = json.loads(r.content)
            self.api_token = res['api_token']
            self.program = res['id']

        # Existing program
        else:
            self.program = program
            self.api_token = api_token

        # Add program to kwargs
        kwargs["program"] = self.program
        kwargs["type"] = "TASK"
        kwargs["name"] = name

        # Init record
        Record.__init__(self, **kwargs)

    def send_records(self, records):

        r = requests.post(
            "{}/api/records/new/{}".format(self.server, self.program),
            params={"token": self.api_token},
            json={"records": [record.dict() for record in records]})

        return json.loads(r.content)


USER_TOKEN = "Fgv9KVIZjTvJ5F2cZsxoesimkry-vaWcY9bxrf3oPlV9TbK2zVBgt8XK8BDgdlUW"
LOREM_IPSUM = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
giat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.
"""
SAMPLE_ERROR = """
Exception in thread django-main-thread:
Traceback (most recent call last):
  [...]
  File "/home/tianshu/projects/checkin/checkin/checkin/urls.py", line 25, in <module>
    path('api/', include('api.urls'))
  File "/home/tianshu/.local/lib/python3.6/site-packages/django/urls/conf.py", line 34, in include
    urlconf_module = import_module(urlconf_module)
  File "/usr/lib/python3.6/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 994, in _gcd_import
  File "<frozen importlib._bootstrap>", line 971, in _find_and_load
  File "<frozen importlib._bootstrap>", line 955, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 665, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 678, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "/home/tianshu/projects/checkin/checkin/api/urls.py", line 2, in <module>
    from . import node
  File "/home/tianshu/projects/checkin/checkin/api/node.py", line 5, in <module>
    from .util import json_response
  File "/home/tianshu/projects/checkin/checkin/api/util.py", line 8
    type(out) == tuple:
                      ^
SyntaxError: invalid syntax
"""

p = Program(
    server="http://localhost:8000", user_token=USER_TOKEN,
    name="Test Program @ " + str(uuid.uuid1()),
    desc="Program description; this program does:" + LOREM_IPSUM).start()
st1 = p.subtask(
    name="Test Parent",
    desc="Test description").start()
info = st1.info(
    name="Test Info",
    desc="Info description\n" + LOREM_IPSUM)
warning = st1.warning(
    name="Test Warning",
    desc="Warning metadata and information")
qt = p.subtask(
    name="Queued Task",
    desc="This task is not yet running.")
err = qt.error(
    name="Test Error",
    desc="Error traceback\n" + SAMPLE_ERROR)

print(p.dict())

print(p.send_records([p, st1, info, warning, qt, err]))

input()
st1.done()
p.send_records([st1])
input()
qt.start()
p.send_records([qt])
input()
qt.done()
p.done()
p.send_records([p, qt])
