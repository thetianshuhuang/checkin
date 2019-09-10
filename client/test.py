import requests
import json
import uuid
import threading
import time


def send_records(
        records, server="http://localhost:8000", program=0, api_token=None):
    """Send records to a server; non-blocking.

    Use this function to send multiple updates at once to cut down on overhead
    waste.

    Parameters
    ----------
    records : Record[]
        List of record objects to send.

    Keyword Args
    ------------
    server : str
        Server to send to.
    program : int
        Program ID
    api_token : str
        Program API acess token
    """

    # Convert to dict if necessary
    records_cvt = [
        record if type(record) == dict else record.dict()
        for record in records]

    def f():
        requests.post(
            "{}/api/records/new/{}".format(server, program),
            params={"token": api_token}, json={"records": records_cvt})

    threading.Thread(target=f).start()


class Record:
    """Generic Record Class

    Keyword Args
    ------------
    name : str
        Record name
    desc : str
        Record description. Newlines are rendered correctly; HTML code will
        be rendered correctly in most situations.
    parent : str or None
        Parent ID. If None, the parent is assumed to be the program.
    record_id : str or None
        Record ID. If None, a new record ID is generated (using uuid4)
    type : str
        Record type. Should be "TASK", "ERR", "WARN", "INFO".
    server : str
        Server address, with port included
    api_token : str
        API access token.
    program : int
        Program ID
    update : bool
        If True, sends a update to the server. Otherwise, the server is not
        notified of record creation. Pass False if multiple updates are to
        be grouped together.
    """

    def __init__(
            self,
            name="Generic Record",
            desc="",
            parent=None,
            record_id=None,
            type="TASK",
            server=None,
            api_token=None,
            program=None,
            update=True):

        assert(api_token is not None)
        assert(server is not None)
        assert(program is not None)

        # Server info
        self.program = program
        self.api_token = api_token
        self.server = server

        # Metadata
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

        # Update server?
        if update:
            self.send_custom_record(**self.dict())

    def send_custom_record(self, **kwargs):
        """Update server with a custom set of parameters.

        The record_id is automatically appended.

        Parameters
        ----------
        **kwargs : dict
            Arguments to send.

        Returns
        -------
        dict
            Server response.
        """

        # Update with record ID
        kwargs.update({"record_id": self.record_id})

        return send_records(
            [kwargs],
            server=self.server,
            program=self.program,
            api_token=self.api_token)

    def subrecord(self, **kwargs):
        """Create sub-record.

        Keyword args are passed on to Record.__init__, with program, server,
        api_token inherited, and parent set to this record's ID.
        """

        if self.type != 'TASK':
            raise Exception("Only TASK records can have sub-records.")

        return Record(
            program=self.program,
            server=self.server,
            api_token=self.api_token,
            parent=self.record_id,
            **kwargs)

    def subtask(self, **kwargs):
        """Alias for Record.subrecord(type="TASK", **kwargs)."""
        return self.subrecord(type="TASK", **kwargs)

    def error(self, **kwargs):
        """Alias for Record.subrecord(type="ERR", **kwargs)."""
        return self.subrecord(type="ERR", **kwargs)

    def warning(self, **kwargs):
        """Alias for Record.subrecord(type="WARN", **kwargs)."""
        return self.subrecord(type="WARN", **kwargs)

    def info(self, **kwargs):
        """Alias for Record.subrecord(type="INFO", **kwargs)."""
        return self.subrecord(type="INFO", **kwargs)

    def dict(self):
        """Get serialized representation of this record.

        Returns
        -------
        dict
            Dictionary with proper entries to update the server. Note that
            server metadata (server, api_token) are not included.
        """
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

    def start(self, update=True):
        """Start timekeeping.

        Keyword Args
        ------------
        update : bool
            If True, updates the server with this task's start time.

        Returns
        -------
        self
            Allow method chaining.
        """
        if self.start_time is not None:
            raise Exception(
                "Could not mark start time: record already started")
        self.start_time = time.time()

        if update:
            self.send_custom_record(start=self.start_time)

        return self

    def done(self, update=True):
        """End timekeeping.

        Keyword Args
        ------------
        update : bool
            If True, updates the server with this task's end time.

        Returns
        -------
        self
            Allow method chaining.
        """
        if self.start_time is None:
            raise Exception(
                "Could not mark finish time: record not yet started")
        if self.end_time is not None:
            raise Exception(
                "Could not mark finish time: record already done")
        self.end_time = time.time()

        if update:
            self.send_custom_record(end=self.end_time)

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
            api_token = res['api_token']
            program = res['id']

        # Init record
        Record.__init__(
            self, program=program, server=server, api_token=api_token,
            type="TASK", name=name, **kwargs)
