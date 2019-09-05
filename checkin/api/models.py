from django.db import models
from django.contrib.auth.models import User


class Program(models.Model):
    """Program; consists of a set of records."""

    # Owner (user)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL)

    # Access token (for APIs)
    api_token = models.TextField()
    # Share token
    share_token = models.TextField()

    # Start time; NULL if not started
    start = models.DateTime()
    # End time; NULL if not done
    end = models.DateTime()


class RunNodes(models.Model):
    """Track compute nodes assigned to each program."""

    # Parent program
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    # Node ID
    node_id = models.TextField()

    # Friendly name
    name = models.TextField()


class Record(models.Model):
    """Task, Error, Warning, or Info Record"""

    # Program ID
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    # UUID corresponding to this record
    record_id = models.CharField(max_length=50)

    # UUID corresponding to record's parent. If this is the root record, the
    # UUID will be nil (00000000-0000-0000-0000-000000000000)
    parent = models.CharField(max_length=50)

    # Record name. For errors, this corresponds to the error name.
    name = models.TextField()
    # Record description. For errors, this corresponds to the traceback.
    desc = models.TextField()

    # Source node ID.
    node_id = models.ForeignKey(RunNodes, on_delete=models.CASCADE)

    # Record type: TASK, ERR, WARN, INFO, META
    type = models.CharField(max_length=10)

    # Start Time; NULL if task not started
    start = models.DateTimeField()

    # End Time; NULL if task not complete
    end = models.DateTimeField()

    # Additional metadata (JSON)
    meta = models.TextField()
